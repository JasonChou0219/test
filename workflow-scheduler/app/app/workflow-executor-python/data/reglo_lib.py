# Written by Valeryia Sidarava and Lukas Bromig at TU Munich
# Institute of Biochemical Engineering
# Lukas.bromig@tum.de, valeryia.sidarava@tum.de
#
# Technical Support Ismatec Reglo ICC :
# Tel: 09377920344
# E-Mail: http://www.ismatec.de/download/documents/IDX1798-PD-IS_lr.pdf
import logging
from requests import get
from time import time


target_service_hostname = "http://localhost"  # -> to env var
target_service_port = '80'  # settings.BACKEND_GATEWAY_UVICORN_PORT  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}:{target_service_port}{target_service_api_version}/'
ADDRESS = 1
route = f"{target_service_url}functions/unobservable/"


class Pump:
    """Volume at Rate mode and Time at Rate mode"""

    def __init__(self, pump: dict):
        self.pump = pump

    def disable_channel_addressing(self):
        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on). If it is already enabled, then the command is skipped
        is_channel_addressing = get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                                   'function_identifier': 'GetChannelAddressing', 'is_property': False,
                                                   'parameters': [ADDRESS],
                                                   'response_identifiers': 'ChannelAddressing'}
                                    ).json()['response']['ChannelAddressing']
        if is_channel_addressing is False:
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                               'function_identifier': 'SetChannelAddressing', 'is_property': False,
                               'parameters': {'Address': ADDRESS, 'ChannelAddressing': True}})

    def pump_set_volume_at_flow_rate(self, flow_rate=None, channels=[1, 2], volume=[80, 80],
                                     direction=['K', 'K']):
        """
        Method to dispense a set volume (mL, max 2 decimal places, in a list []) with a set flow rate (mL/min, max 2
        decimal places, in a list []), rotation direction (J=clockwise, K=counter-clockwise, in a list []) for specific
        channel or channels.
        Pump address for Reglo ICC is set on 1, yet can be changed with SetPumpAddress function

        If several channels are used, there must be same number of values in each other parameter, except for pump
        and return_val.
        """
        return_val = ''
        start_time0 = time()
        self.disable_channel_addressing()

        # Checks whether the flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            flow_rate_at_mode = get(route, params={'service_uuid': self.pump['uuid'],
                                                   'feature_identifier': 'ParameterController',
                                                   'function_identifier': 'GetFlowRateAtModes', 'is_property': False,
                                                   'parameters': [ADDRESS],
                                                   'response_identifiers': 'CurrentFlowRate'}).json()['response']['CurrentFlowRate']
            if flow_rate_at_mode is False:
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                   'function_identifier': 'SetFlowRateMode', 'is_property': False,
                                   'parameters': [channel]})

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                max_flow_rate_with_cal = get(route, params={'service_uuid': self.pump['uuid'],
                                                            'feature_identifier': 'ParameterController',
                                                            'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                            'is_property': False,
                                                            'parameters': [channel],
                                                            'response_identifiers': 'MaximumFlowRateWithCalibration'}
                                             ).json()['response']['MaximumFlowRateWithCalibration']
                print('Max flow rate is: ', max_flow_rate_with_cal)
                flow_rate.append(max_flow_rate_with_cal)  # [:6])
            logging.info('Calibrated maximum flow rate used: ', flow_rate)
        
        # Iteration: for each channel the following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Volume at Rate mode, which allows to dispense a set volume with a set flow rate
            current_pump_mode = get(route,
                                    params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                            'function_identifier': 'GetMode', 'is_property': False,
                                            'parameters': [channel],
                                            'response_identifiers': 'CurrentPumpMode'}).json()['response']['CurrentPumpMode']
            print('####################')
            print(current_pump_mode)
            if current_pump_mode != 'O':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                   'function_identifier': 'SetVolumeRateMode', 'is_property': False,
                                   'parameters': [channel]})

            # The volume to dispense is set according to the setting in the head of the function (in mL)
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                               'function_identifier': 'SetVolume', 'is_property': False,
                               'parameters': {'Channel': channel, 'Volume': volume[i]}})

            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                               'function_identifier': 'SetFlowRate', 'is_property': False,
                               'parameters': {'Channel': channel, 'SetFlowRate': flow_rate[i]}})

            # Gets the current direction direction of the channel and compares to the desired setting. If the settings
            # do not match, the sets it to counter-clockwise ...
            pump_direction = get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                                'function_identifier': 'GetPumpDirection', 'is_property': False,
                                                'parameters': [channel],
                                                'response_identifiers': 'PumpDirection'}).json()['response']['PumpDirection']
            if pump_direction != direction[i] and direction[i] == 'K':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                   'function_identifier': 'SetDirectionCounterClockwise', 'is_property': False,
                                   'parameters': [channel]})
            # ... or clockwise rotation direction
        
            elif pump_direction != direction[i] and direction[i] == 'J':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                   'function_identifier': 'SetDirectionClockwise', 'is_property': False,
                                   'parameters': [channel]})
        
        start_time = time()    # Notes the time
        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                               'function_identifier': 'StartPump', 'is_property': False,
                               'parameters': [channel]})
            return_val = f'Volume at Rate mode on channel {channel} for volume {volume[i]} mL at rate {flow_rate[i]} ' \
                         f'mL/min set \n'
        # logging.info('--- Total execution time: %s seconds ---' %((time.time()-start_time0)))
        return return_val

    def pump_time_at_flow_rate(self, flow_rate=None, channels=[1, 2], runtime=['10.5', '5.3'],
                               direction=['K', 'K']):
        """
        Method to dispense for a set time duration (seconds, max 1 decimal place, in a list []) with a set flow rate
        (mL/min, max 2 decimal places, in a list []), rotation direction (J=clockwise, K=counter-clockwise, in a
        list []) for specific channel or channels.
        Pump address for Reglo ICC is set on 1, yet can be changed with SetPumpAddress function

        If several channels are used, there must be same number of values in each other parameter, except for pump and
        return_val.
        """
        return_val = ''

        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        self.disable_channel_addressing()

        # checks, whether flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            is_at_flow_rate_mode = get(route, params={'service_uuid': self.pump['uuid'],
                                                      'feature_identifier': 'ParameterController',
                                                      'function_identifier': 'GetFlowRateAtModes', 'is_property': False,
                                                      'parameters': [channel],
                                                      'response_identifiers': 'CurrentFlowRate'}
                                       ).json()['response']['CurrentFlowRate']
            if is_at_flow_rate_mode is False:
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                   'function_identifier': 'SetFlowRateMode', 'is_property': False,
                                   'parameters': {'Channel': channel, 'ChannelAddressing': True}})

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                max_flow_rate_with_cal = get(route, params={'service_uuid': self.pump['uuid'],
                                                            'feature_identifier': 'ParameterController',
                                                            'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                            'is_property': False,
                                                            'parameters': [channel],
                                                            'response_identifiers': 'MaximumFlowRateWithCalibration'}
                                             ).json()['response']['MaximumFlowRateWithCalibration']
                flow_rate.append(max_flow_rate_with_cal)
            logging.info('Calibrated maximum flow rate used: ', flow_rate)

        # Iteration: for each channel following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Time mode, with allows to dispense for a set time duration with a set flow rate
            current_pump_mode = get(route,
                                    params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                            'function_identifier': 'GetMode', 'is_property': False,
                                            'parameters': [channel],
                                            'response_identifiers': 'CurrentPumpMode'}).json()['response']['CurrentPumpMode']
            if current_pump_mode != 'N':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                   'function_identifier': 'SetTimeMode', 'is_property': False,
                                   'parameters': [channel]})

            # The time duration to dispense is set according to the setting in the head of the function (in seconds with
            # max. 1 decimal place)
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                               'function_identifier': 'SetCurrentRunTime', 'is_property': False,
                               'parameters': {'Channel': channel, 'RunTime': runtime[i]}})
            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                               'function_identifier': 'SetFlowRate', 'is_property': False,
                               'parameters': {'Channel': channel, 'SetFlowRate': flow_rate[i]}})

            # Gets the current rotation direction of the channel and compares to the desired setting. If the settings do
            # not match, the sets it to counter-clockwise ...
            pump_direction = get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                                'function_identifier': 'GetPumpDirection', 'is_property': False,
                                                'parameters': [channel],
                                                'response_identifiers': 'PumpDirection'}).json()['response']['PumpDirection']
            if pump_direction != direction[i] and direction[i] == 'K':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                   'function_identifier': 'SetDirectionCounterClockwise', 'is_property': False,
                                   'parameters': [channel]})
            # ... or clockwise rotation direction

            elif pump_direction != direction[i] and direction[i] == 'J':
                get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                   'function_identifier': 'SetDirectionClockwise', 'is_property': False,
                                   'parameters': [channel]})

        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                               'function_identifier': 'StartPump', 'is_property': False,
                               'parameters': [channel]})
            return_val = f'Time mode on channel {channel} for time {runtime[i]} seconds at rate {flow_rate[i]} ' \
                         f'mL/min set \n\n'
        return return_val

    def pump_stop(self, channels=[1, 2]):
        """
        Method to stop the channel(s).
        """
        return_val = ''
        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        self.disable_channel_addressing()

        for channel in channels:
            get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                               'function_identifier': 'StopPump', 'is_property': False,
                               'parameters': [channel]})
            return_val = f'Channel {channel} stopped \n\n'
        return return_val

    def pump_status(self):
        """
        Method to check whether the pump is currently running (+) or not (-).

        If one or more channels are in use, the status would be 'running'. However, it is impossible to distinguish,
        which and how many channels are used.
        """

        return_val = get(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                        'function_identifier': 'GetPumpStatus', 'is_property': False,
                                        'parameters': [ADDRESS],
                                        'response_identifiers': 'CurrentPumpStatus'}).json()['response']['CurrentPumpStatus']
        return return_val
