import time
import numpy as np
import devices
import interface.DASGIP.DASGIP_Service.DASGIP_Service_client as client
import logging
import pandas


def initialize_logging():
    # initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # file handler
    filehandler = logging.FileHandler(__file__ + '.log', mode='a')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    # console handler, i.e. output to command window
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def start_feed_pump(reactor_client, units: list):
    """ Start reactor feed pump C of the reactor """
    for unit in units:
        reactor_client.PumpCServicer_SetCmd(unit, 2)


def stop_feed_pump(reactor_client, units):
    """ Stop reactor feed pump C of the reactor """
    for unit in units:
        reactor_client.PumpCServicer_SetCmd(unit, 1)


def calculate_pump_duration(elapsed_time: float, feed_rate: float, pump_rate: float):
    """ Calculates the time the pump must run to transfer a discrete volume  """
    volume_to_pump = (elapsed_time / 60) * feed_rate  # feed rate has the unit ml/h, elapsed time has the unit minutes
    logger.info(f'The volume to pump is {volume_to_pump}')
    pump_time_min = (volume_to_pump / pump_rate) * 60  # pump rate has the unit ml/h
    return pump_time_min


if __name__ == '__main__':
    # Instantiate the devices
    reactor_client = devices['DasgipService']()
    offgas_analytics_client = devices['BlueVaryService']()
    external_pump_client = devices['RegloICCService']()

    # Instantiate database client

    # Instantiate logging
    logger = initialize_logging()

    # Define process parameter variables
    reactor_units = [0, 2]   # 0-based counting
    reactor_pump_rate = 40   # The applied pump rate in the reactor, in this case max rate is used
    reactor_feed_rate = 2.4  # Total feed rate in ml / h
    experiment_duration = 16 * 60 * 60
    increment = 0.1


    # Import the discrete substrate addition times and volumes from an external file
    df_feeding_intervals = pandas.read_csv("feeding_interval.csv")
    print(df_feeding_intervals)
    feed_intervals = df_feeding_intervals['time_interval, min']
    print(feed_intervals)

    # Set initial pump rate, avoids manual work
    for reactor_unit in reactor_units:
        # Set reactor feed pump setpoints
        reactor_client.PumpCServicer_SetSetpointSelect(reactor_unit, 1)
        reactor_client.PumpCServicer_SetSPM(reactor_unit, reactor_pump_rate)
    logger.info(f'Setpoint is set to {reactor_pump_rate} ml/h for the units {reactor_units}')

    # Start of the main loop
    experiment_start_time = time.time()
    start_time = time.time()
    logger.info(f' Start time is {start_time}')
    # Iterate over the discrete entries of feeding events in the file to simulate an intermittent feeding strategy
    # with a peristaltic pump in a L-scale fermenter
    for index, off_timer in feed_intervals.items():
        exit_criterion: bool = False
        delta_t: float = 0

        # Wait for the off-timer to elapse
        logger.debug(f'Waiting for off-timer ({off_timer}) to elapse')
        # We wait until the next feeding event is reached

        while delta_t < off_timer:
            if time.time() >= (experiment_start_time + experiment_duration):
                # If the defined experiment duration is reached, the exit procedure is initiated
                logger.debug(f'Exiting experiment main loop at {time.time()}/ {experiment_start_time + experiment_duration}')
                exit_criterion = True
                break
            time.sleep(increment)
            delta_t = (time.time() - start_time) / 60

        if exit_criterion:
            # break out of the for-loop
            break
        # Re-initialize the start time while the pump is working
        start_time = time.time()
        logger.info(f' Start time is {start_time}')

        # Pump the desired volume while the off-timer starts to elapse
        pump_time_min = calculate_pump_duration(elapsed_time=off_timer, feed_rate=reactor_feed_rate, pump_rate=reactor_pump_rate)
        logger.info(f'The scheduled pump run time in minutes is {pump_time_min}')

        # Start the pump
        start_feed_pump(reactor_client=reactor_client, units=reactor_units)
        time.sleep(pump_time_min)
        # Stop the pump
        stop_feed_pump(reactor_client=reactor_client, units=reactor_units)
