# Written by Lukas Bromig, Institute of Biochemical Engineering at TU Munich (17.06.2021)
import time
import signal
import logging
import csv
import smtplib, ssl
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# PRESETS
logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d | %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# in g/mL -> 1000 kg/m^3
FLUID_DENSITY = 1

# (rpm, duration in s)
calibration_points = [
    (50, 60),
    (100, 60),
    (150, 30),
    (200, 30)
]


def run(services):

    # INITIALIZATION
    services = initialize_services(services)
    pump = services['RegloDCService']
    balance = services['MT_Viper_SW_Balance_Service']

    pump.call_command("DriveControlServicer", "SetDirectionClockwise", parameters={})
    pump.call_command("DeviceServicer", "LockControlPanel", parameters={})
    pre_pump(pump=pump)

    calibration_rpm = [0]
    calibration_flow_rate = [0]
    calibration_duration =[0]
    calibration_weight = [0]

    # MEASURE

    for i, calibration_point in enumerate(calibration_points):
        rpm_setpoint = calibration_point[0]
        duration = calibration_point[1]
        logger.info(f'Calibration point {i}.{rep}: Running at {rpm_setpoint} rpm for {duration} seconds')
        pump.call_command("ParameterControlServicer", "SetRPM", parameters = { "RPM/Real": rpm_setpoint })
        initial_weight = get_weight(client=balance)
        logger.info(f'Initial weight: {initial_weight}')

        pump.call_command("DriveControlServicer", "StartPump", parameters={})

        time.sleep(duration)

        pump.call_command("DriveControlServicer", "StopPump", parameters={})
        time.sleep(4)
        final_weight = get_weight(client=balance)
        logger.info(f'Final weight: {final_weight}')

        weight_difference = final_weight - initial_weight
        logger.info(f'Weight difference: {weight_difference}')
        flow_rate = (weight_difference/FLUID_DENSITY)/duration  # in mL/s
        logger.info(f'Flowrate: {flow_rate}')

        calibration_rpm.append(calibration_point[0])
        calibration_flow_rate.append((flow_rate))
        calibration_duration.append(calibration_point[1])
        calibration_weight.append(weight_difference)

    pump.call_command("DeviceServicer","UnlockControlPanel", parameters={})

    # ANALYSE AND SAVE DATA
    file_names = save_data(calibration_rpm, calibration_flow_rate, calibration_duration, calibration_weight)
    send_mail(attachments=file_names)


def initialize_services(services: list = None):
    _initialized_service_clients = {}
    for service in services:
        try:
            service.connect()
            _initialized_service_clients[service.name] = service
            logger.info(f'Service successfully instantiated and connected: {service.name}@{service.ip}:{service.port}')
        except Exception as e:
            logger.error(f'Failed to connect to {service.name}. Service not instantiated!')
            logger.exception(e)
    return _initialized_service_clients


def pre_pump(pump):
    logger.info('Pre-pumping liquid...')
    _rpm = 200
    _duration = 10
    pump.call_command("ParameterControlServicer", "SetRPM", parameters = { "RPM/Real": _rpm })
    pump.call_command("DriveControlServicer", "StartPump", parameters={})
    time.sleep(_duration)
    pump.call_command("DriveControlServicer", "StopPump", parameters={})
    time.sleep(3)


def get_weight(client):
    while True:
        try:
            weight = client.call_property("org.silastandard/examples/BalanceService/v1","StableWeightValue")['stableweightvalue/constrained/real']
            # logger.info(f'Measured stable weight: {weight}')
            break
        except Exception as e:
            logger.exception(e)
            logger.error(f'ValueError encountered')
            # Wait 5 seconds before retry
            time.sleep(5)
            continue
    return weight


def save_data(calibration_rpm, calibration_flow_rate, calibration_duration, calibration_weight):
    # Plot data

    gradient, intercept, r_value, p_value, std_err = stats.linregress(calibration_rpm, calibration_flow_rate)
    mn = np.min(calibration_rpm)
    mx = np.max(calibration_rpm)
    x1 = np.linspace(mn, mx, 500)
    y1 = gradient*x1+intercept
    plt.plot(calibration_rpm, calibration_flow_rate, 'ob')
    plt.plot(x1,y1,'-r')
    plt.title('Pump calibration')
    plt.ylabel('Flow rate in mL/s')
    plt.xlabel('rpm in 1/min')
    plt.xlim(0)
    plt.ylim(0)
    plt.text(x=0, y=(np.max(calibration_flow_rate)*0.9), s=f' y = {gradient:.4f} * x + {intercept:.4f}\n R: {r_value:.4f}\n P: {p_value:.4f}')
    timestamp = datetime.now()
    file_name_plot = f'Pump_calibration_{timestamp.year}_{timestamp.month}_{timestamp.day}.png'
    plt.savefig(file_name_plot)


    # Save data as csv
    file_name_data = 'calibration_data.csv'
    with open(file_name_data, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Calibration point', 'rpm_setpoint in 1/min', 'calibration_duration in s', 'calibration_weight in g', 'calibration_flow_rate in mL/s'])
        for i, row in enumerate(calibration_rpm):
            writer.writerow([i, calibration_rpm[i], calibration_duration[i], calibration_weight[i], calibration_flow_rate[i]])


    return [file_name_plot, file_name_data]


def send_mail(attachments):
    sender_email = input("Type your sender email and press enter:")
    receiver_email = input("Type your receiver email and press enter:")
    password = input("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "BIOLAGO HACKATHON pump calibration results"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    These are the latest pump calibration results!
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    for f in attachments or []:
        with open(f, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        message.attach(part)
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first



    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
