import time
import signal
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import csv


class PumpClient:
    """This is a simulation client"""
    ip = '127.0.0.1'
    port = 50051
    rpm = 0

    def __init__(self):
        self.command_dict = {
            'StartPump': self.no_func,
            'SetDirectionClockwise': self.no_func,
            'SetDirectionCounterClockwise': self.no_func,
            'UnlockControlPanel': self.no_func,
            'LockControlPanel': self.no_func,
            'SetRPM': self.set_rpm,
            'GetRPM': self.set_rpm,
            'SetDisplayLetters': self.no_func,
            'StopPump': self.no_func,
        }

    def call_command(self, feature_identifier, command_identifier, parameters):
        func = self.command_dict[command_identifier]
        return func(parameters)

    def set_rpm(self, parameters = None):
        if not parameters is None:
            self.rpm = parameters
        return self.rpm

    def no_func(self, parameter):
        return True


class BalanceClient:
    """This is a simulation client"""
    ip = '127.0.0.1'
    port = 50052
    t_0 = time.time()

    weight = 0

    def __init__(self):
        self.command_dict = {
            'ShowWeight': self.no_func,
        }
        self.property_dict = {
            'StableWeightValue':self.get_weight,
        }

    def call_command(self, feature_identifier, command_identifier, parameters):
        func = self.command_dict[command_identifier]
        return func(parameters)

    def call_property(self, feature_identifier, property_identifier):
        func = self.property_dict[property_identifier]
        return func()

    def get_weight(self):
        time.time() - self.t_0
        self.weight = time.time() - self.t_0 + np.random.rand()
        return self.weight

    def no_func(self, parameter):
        return True


services = {
    'RegloDCService': PumpClient,
    'MT_Viper_SW_Balance_Service': BalanceClient,
}


logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d | %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# in g/mL -> 1000 kg/m^3
FLUID_DENSITY = 1

# (rpm, duration in s)
calibration_points = [
    (50, 6),
    (100, 6),
    (150, 3),
    (200, 3)
]


def run(services):
    pump_client = services['RegloDCService']()
    print(f'Pump instantiated at {pump_client.ip}:{pump_client.port}')
    balance_client = services['MT_Viper_SW_Balance_Service']()
    print(f'Balance instantiated at {balance_client.ip}:{balance_client.port}')
    print('Done')
    pump_client.call_command("DriveControlServicer", "SetDirectionClockwise", parameters={})
    pump_client.call_command("DeviceServicer", "LockControlPanel", parameters={})
    #pre_pump(pump_client=pump_client)

    calibration_rpm = [0]
    calibration_flow_rate = [0]
    calibration_duration =[0]
    calibration_weight = [0]

    for i, calibration_point in enumerate(calibration_points):

        rpm_setpoint = calibration_point[0]
        duration = calibration_point[1]
        print(f'Calibration point {i}: Running at {rpm_setpoint} rpm for {duration} seconds')
        pump_client.call_command("ParameterControlServicer", "SetRPM", rpm_setpoint)
        initial_weight = balance_client.call_property("org.silastandard/examples/BalanceService/v1", "StableWeightValue")  # ['stableweightvalue/constrained/real']
        pump_client.call_command("DriveControlServicer", "StartPump", parameters={})
        time.sleep(duration)
        pump_client.call_command("DriveControlServicer", "StopPump", parameters={})
        final_weight = balance_client.call_property("org.silastandard/examples/BalanceService/v1", "StableWeightValue")  # ['stableweightvalue/constrained/real']
        weight_difference = final_weight - initial_weight
        print(f'Weight difference: {weight_difference}')
        flow_rate = (weight_difference/FLUID_DENSITY)/duration  # in mL/s
        print(f'Flowrate: {flow_rate}')

        calibration_rpm.append(calibration_point[0])
        calibration_flow_rate.append((flow_rate))
        calibration_duration.append(calibration_point[1])
        calibration_weight.append(weight_difference)

    file_names = save_data(calibration_rpm, calibration_flow_rate, calibration_duration, calibration_weight)
    send_mail(attachments=file_names)


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


def pre_pump(pump_client):
    print('Pre-pumping liquid...')
    _rpm = 200
    _duration = 10
    pump_client.call_command("ParameterControlServicer", "SetRPM", _rpm)
    pump_client.call_command("DriveControlServicer", "StartPump", parameters={})
    time.sleep(_duration)
    pump_client.call_command("DriveControlServicer", "StopPump", parameters={})


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


if __name__=='__main__':
    run(services=services)
