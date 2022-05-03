import time
from time import sleep, time
import logging
import json
from requests import post, get
import data.reglo_lib as RLib

target_service_hostname = "http://10.152.248.14"  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}{target_service_api_version}/'

# Connect the clients of the RegloICC and the MT Viper SW. This should happen automatically in the __main__.py in the
# container when it is started. Connection details are supplied by the workflow scheduler.
route = f"{target_service_url}functions/connect_initial"  # Should be connect only, but return of connect does not

pump = get(route, params={'client_ip': '10.152.248.24', 'client_port': 50101})
pump = pump.json()
print(pump, flush=True)

dasgip = get(route, params={'client_ip': '10.152.248.24', 'client_port': 50100})
dasgip = dasgip.json()
print(dasgip, flush=True)

services_dict = {
    'RegloICC': pump,
    'DASGIP': dasgip,
}

# TODO: Suitable accompanying configurations for the dasgip plant, i.e. stirrer speed, gassing rate, temperature
#  during medium exchange
ROUTE = f"{target_service_url}functions/unobservable"
logger = logging.getLogger(name='__main__')

# Adjust the following parameters to parametrize the experiment!
UNIT = 0  # Reactor unit, 0 based counting
PUMP_ADDRESS = 1
MIN_MEDIUM_EXCHANGE_INTERVAL = 600  # 600 s
REACTOR_VOLUME = 575  # mL  575
BATCH_PHASE_ESTIMATION = 1 * 60 * 60  # Estimation of the minimum length of the batch phase in seconds
# BATCH_PHASE_ESTIMATION = 1 * 60 * 60  # in this case 3 hours
MAX_VOLUME_LEVEL = 200  # muS
PUMP_CHANNEL_IN = 1  # Pumping in on channel 1 in direction "K", counter-clockwise
PUMP_CHANNEL_OUT = 2  # Pumping out on channel 2 in direction "J", clockwise.


class ALEMediumExchange:
    # Variables that need to be predefined to be given to the functions
    # Last time when the medium was exchanged, at start the script start
    last_medium_exchange = time()  # Bool if the batch phase is currently ongoing (and detected)
    batch_phase_ongoing = False  # Bool if the medium should be exchanged right now
    is_medium_exchange_needed = False
    # Condition that should abort the experiment, will be altered if the safety timer for the medium exchange
    # is triggered
    abort_condition = False
    safety_timer_limit = 25 * 60  # Timer for the pump in seconds, initial guess, will be corrected at runtime
    start_time = time()  # Start time of the script

    def __init__(self, service_dict):
        logger.info('New run started')
        # Objects of pump and dasgip to control both
        self.pump = service_dict['RegloICC']
        self.dasgip = service_dict['DASGIP']
        # A library with convenience methods for pump control
        self.pump_lib = RLib.Pump(pump=self.pump, address=PUMP_ADDRESS, route=ROUTE)

    # This method is supposed to be called when the pump is working and you want to know when it is finished
    def wait_for_pump_finish(self, timeout=None):
        if timeout is None:
            while True:
                if self.pump_lib.pump_status() == '+':
                    logger.debug('Pump is still working')
                    sleep(2)
                if self.pump_lib.pump_status() == '-':
                    logger.info('Pump finished')
                    return
        if timeout is not None:
            pump_time = 0
            pump_start_time = time()
            while pump_time < timeout:
                if self.pump_lib.pump_status() == '+':
                    logger.debug('Pump is still working')
                    time.sleep(1)
                    pump_time = time() - pump_start_time
                if self.pump_lib.pump_status() == '-':
                    logger.info('Pump finished')
                    return
            logger.error('Wait for pump finish has been cancelled because of the timeout')
            return

    # This function will remove a certain volume via channel 1 and add the same amount of medium via channel 2 back to
    # the reactor
    def change_medium(self, volume):
        # Disable temperature control and ph control (open loop otherwise)
        temp_cmd_mode_1 = post(ROUTE,
                               params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'TemperatureServicer',
                                       'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                               data=json.dumps({"UnitID": UNIT,
                                                "Cmd": 2})).json()['response']['CmdSet']
        logger.debug(f'temp_cmd_mode_1 is: {temp_cmd_mode_1}')
        ph_cmd_mode_1 = post(ROUTE,
                             params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'PHServicer',
                                     'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                             data=json.dumps({"UnitID": UNIT,
                                              "Cmd": 1})).json()['response']['CmdSet']
        logger.debug(f'ph_cmd_mode_1 is: {ph_cmd_mode_1}')

        self.abort_condition = False
        self.batch_phase_ongoing = False
        self.is_medium_exchange_needed = False
        logger.info('Starting medium exchange')
        # safety_timer = 20 * 60

        # Remove initial volume
        print(self.pump_lib.pump_set_volume_at_flow_rate(channels=[PUMP_CHANNEL_OUT], volume=[volume], direction=['J']))
        self.wait_for_pump_finish()
        logger.info('Medium removal finished')

        # Add volume based on antifoam sensor and safety_timer
        stirrer_cmd_mode_1 = post(ROUTE,
                                  params={'service_uuid': self.dasgip['uuid'],
                                          'feature_identifier': 'AgitationServicer',
                                          'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                                  data=json.dumps({"UnitID": UNIT,
                                                   "Cmd": 1})
                                  ).json()['response']['CmdSet']
        logger.debug(f'stirrer_CmdMode1 is: {stirrer_cmd_mode_1}')

        # Stop stirrer before pumping in fresh medium to be able to detect the level using the capacitive sensor
        print(
            self.pump_lib.pump_time_at_flow_rate(channels=[1], runtime=[self.safety_timer_limit * 2], direction=['J']))

        safety_start_time = time()
        logger.info(f'The current safety_timer_limit is {self.safety_timer_limit}')
        safety_timer = 0
        level_sensor_pv = post(ROUTE,
                               params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'LevelServicer',
                                       'function_identifier': 'GetPV',
                                       'response_identifiers': "CurrentPV"},
                               data=json.dumps({"UnitID": UNIT})
                               ).json()['response']['CurrentPV']
        logger.debug(f'level_sensor_pv is: {level_sensor_pv}')
        while safety_timer < self.safety_timer_limit and level_sensor_pv < MAX_VOLUME_LEVEL:
            level_sensor_pv = post(ROUTE,
                                   params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'LevelServicer',
                                           'function_identifier': 'GetPV', 'response_identifiers': "CurrentPV"},
                                   data=json.dumps({"UnitID": UNIT})
                                   ).json()['response']['CurrentPV']
            logger.debug(f'The current level sensor output / conductivity is: {level_sensor_pv}')
            sleep(3)
            safety_timer = time() - safety_start_time
            logger.debug(f'The current time for medium refill is: {safety_timer}')
        self.pump_lib.pump_stop(channels=[PUMP_CHANNEL_IN])
        # Restart the stirrer
        stirrer_cmd_mode_2 = post(ROUTE,
                                  params={'service_uuid': self.dasgip['uuid'],
                                          'feature_identifier': 'AgitationServicer',
                                          'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                                  data=json.dumps({"UnitID": UNIT,
                                                   "Cmd": 2})
                                  ).json()['response']['CmdSet']
        logger.debug(f'stirrer_CmdMode2 is: {stirrer_cmd_mode_2}')

        # Check if the run needs to be aborted because the safety_timer is exceeded
        if safety_timer > self.safety_timer_limit:
            self.abort_condition = True
            self.last_medium_exchange = time()
            logger.error(f'Critical Error! Safety timer({safety_timer}) exceeded safety_timer_limit('
                         f'{self.safety_timer_limit})')
            self.safety_timer_limit = safety_timer
            return

        self.last_medium_exchange = time()

        # Enable temperature control
        temp_cmd_mode_2 = post(ROUTE,
                               params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'TemperatureServicer',
                                       'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                               data=json.dumps({"UnitID": UNIT,
                                                "Cmd": 2})).json()['response']['CmdSet']
        logger.debug(f'temp_CmdMode2 is: {temp_cmd_mode_2}')
        ph_cmd_mode_2 = post(ROUTE,
                             params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'PHServicer',
                                     'function_identifier': 'SetCmd', 'response_identifiers': "CmdSet"},
                             data=json.dumps({"UnitID": UNIT,
                                              "Cmd": 2})
                             ).json()['response']['CmdSet']
        logger.debug(f'ph_CmdMode2 is: {ph_cmd_mode_2}')
        logger.info('Medium addition finished, Medium exchange finished')
        self.safety_timer_limit = safety_timer * 2
        return

    def check_if_batch_phase_ongoing(self):
        # Check if 10 minutes have passed since the last medium exchange
        if self.last_medium_exchange + MIN_MEDIUM_EXCHANGE_INTERVAL < time():
            # Check if the current dissolved oxygen value is below 60%, indicating that the cells are growing
            curr_do = post(ROUTE, params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'DOServicer',
                                          'function_identifier': 'GetPV', 'response_identifiers': "CurrentPV"},
                           data=json.dumps({"UnitID": UNIT})
                           ).json()['response']['CurrentPV']
            logger.debug(f'Check if batch phase ongoing. Checking DO Sensor Output: {curr_do}')
            if curr_do == -1:
                return False
            if curr_do < 50:
                logger.debug(f'The current DO sensor output is: {curr_do}\nBatch phase detected!')
                return True
            else:
                logger.debug('Batch phase was not detected, returning')
                return False
        else:
            logger.debug('Batch phase was not detected. Minimum medium exchange interval not yet elapsed.')
            return False

    def check_if_medium_exchange_needed(self):
        """This function evaluates whether the medium should be exchanged and returns true if the answer is yes"""
        if self.last_medium_exchange + BATCH_PHASE_ESTIMATION < time():
            curr_do = post(ROUTE, params={'service_uuid': self.dasgip['uuid'], 'feature_identifier': 'DOServicer',
                                          'function_identifier': 'GetPV', 'response_identifiers': "CurrentPV"},
                           data=json.dumps({"UnitID": UNIT})
                           ).json()['response']['CurrentPV']
            logger.debug(f'Check if Medium exchange needed. Checking DO Sensor Output: {curr_do}')
            # Todo: Remove. For testing purposes!
            # if curr_do == -1:
            #    return True
            if curr_do > 75:
                logger.info(f'End of Batch phase detected')
                return True
            else:
                logger.debug('DO has not risen again')
                return False
        else:
            logger.debug('Batch phase estimation not elapsed')
            return False

    def start(self):
        # Main loop. Will be completed endless times throughout the experiment. Will re-evaluate if the medium should
        # be exchanged
        i = 0
        self.pump_lib.adjust_pump_settings()
        while not self.abort_condition:
            process_time = (time() - self.start_time) / (60 * 60)
            logger.debug(f'The current process time in hours is: {process_time:.4f}')

            # Check if the batch phase has started in the first place, will not be repeated once the batch phase has
            # been detected
            if not self.batch_phase_ongoing:
                self.batch_phase_ongoing = self.check_if_batch_phase_ongoing()
                logger.debug(f'Batch phase is {"ongoing" if self.batch_phase_ongoing else "not ongoing"}')

            # Test
            # self.batch_phase_ongoing = True
            # Check if the batch phase has started

            if self.batch_phase_ongoing:
                # Check if DO has risen again and if the time has elapsed to exchange the medium
                self.is_medium_exchange_needed = self.check_if_medium_exchange_needed()

            # Testing
            # self.is_medium_exchange_needed = True
            if self.is_medium_exchange_needed is True:
                self.change_medium(volume=REACTOR_VOLUME)
            sleep(5)


# Test block. Delete before use:
# BATCH_PHASE_ESTIMATION = 2 * 60

def run():
    # print('Services', flush=True)
    # print(services, flush=True)
    print('Service_Dict', flush=True)
    print(services_dict, flush=True)
    ale_medium_exchange = ALEMediumExchange(service_dict=services_dict)
    ale_medium_exchange.start()
