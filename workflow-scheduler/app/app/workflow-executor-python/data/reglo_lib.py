# Written by Valeryia Sidarava and Lukas Bromig at TU Munich
# Institute of Biochemical Engineering
# Lukas.bromig@tum.de, valeryia.sidarava@tum.de
#
# Technical Support Ismatec Reglo ICC :
# Tel: 09377920344
# E-Mail: http://www.ismatec.de/download/documents/IDX1798-PD-IS_lr.pdf
import logging
import json
from requests import post
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

    def enable_channel_addressing(self):
        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on). If it is already enabled, then the command is skipped
        is_channel_addressing = \
        response = post(route,
                        params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                'function_identifier': 'GetChannelAddressing',
                                'parameters': [ADDRESS],
                                'response_identifiers': "ChannelAddressing"}
                        # data=json.dumps({"Address": ADDRESS})
                        ).json()
        if is_channel_addressing is False:
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                'function_identifier': 'SetChannelAddressing',
                                'parameters': [ADDRESS, True]}
                 #data=json.dumps({"Address": ADDRESS})
                 )

    def adjust_pump_settings(self):
        self.enable_channel_addressing()
        is_event_messages = \
        post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                            'function_identifier': 'GetEventMessages',
                            'response_identifiers': "EventMessages",
                            'parameters': [ADDRESS]}
             #data=json.dumps({"Address": ADDRESS})
             ).json()['response']['EventMessages']
        if is_event_messages:
            # event_messages_set = pump_client.DeviceService.SetEventMessages(Address=1,
            #                                                                 EventMessages=False).EventMessagesSet
            event_messages_set = post(route, params={'service_uuid': self.pump['uuid'],
                                                     'feature_identifier': 'DeviceService',
                                                     'function_identifier': 'SetEventMessages',
                                                     'response_identifiers': "EventMessagesSet",
                                                     'parameters': [ADDRESS, False]}
                                      #data=json.dumps({"Address": ADDRESS,
                                      #                 "EventMessages": False,
                                      #                 })
                                      ).json()['response'][
                'EventMessagesSet']
            print(f'Event messages are enabled. Disabled event messages: {event_messages_set}')
            is_event_messages = post(route, params={'service_uuid': self.pump['uuid'],
                                                    'feature_identifier': 'DeviceService',
                                                    'function_identifier': 'GetEventMessages',
                                                    'response_identifiers': "EventMessages",
                                                    'parameters': [ADDRESS]}
                                     # data=json.dumps({"Address": ADDRESS})
                                     ).json()['response'][
                'EventMessages']
            print(f'{"Event messages disabled" if not is_event_messages else "Event messages not disabled!"}')

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
        self.enable_channel_addressing()

        # Checks whether the flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            flow_rate_at_mode = post(route, params={'service_uuid': self.pump['uuid'],
                                                    'feature_identifier': 'ParameterController',
                                                    'function_identifier': 'GetFlowRateAtModes',
                                                    'response_identifiers': "CurrentFlowRate",
                                                    'parameters': [ADDRESS]}
                                     # data=json.dumps({"Address": ADDRESS})
                                     ).json()['response'][
                'CurrentFlowRate']
            if flow_rate_at_mode is False:
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                    'function_identifier': 'SetFlowRateMode',
                                    'parameters': [channel]},
                     # data=json.dumps({"Channel": channel})
                     )

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                print('Channel is', channel)
                max_flow_rate_with_cal = post(route, params={'service_uuid': self.pump['uuid'],
                                                             'feature_identifier': 'ParameterController',
                                                             'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                             'response_identifiers': "MaximumFlowRateWithCalibration"},
                                                             # 'parameters': [channel]}
                                              data=json.dumps({"Channel": channel})
                                              ).json()  #  ['response']['MaximumFlowRateWithCalibration']
                max_flow_rate_with_cal = max_flow_rate_with_cal['response']['MaximumFlowRateWithCalibration']
                flow_rate.append(max_flow_rate_with_cal)  # [:6])
            logging.info('Calibrated maximum flow rate used: ', flow_rate)

        # Iteration: for each channel the following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Volume at Rate mode, which allows to dispense a set volume with a set flow rate
            current_pump_mode = post(route,
                                     params={'service_uuid': self.pump['uuid'],
                                             'feature_identifier': 'ParameterController',
                                             'function_identifier': 'GetMode',
                                             'response_identifiers': "CurrentPumpMode",
                                             'parameters': [channel]}
                                     # data=json.dumps({"Channel": channel})
                                     ).json()['response'][
                'CurrentPumpMode']
            print(current_pump_mode)
            if current_pump_mode != 'O':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                    'function_identifier': 'SetVolumeRateMode',
                                    'parameters': [channel]}
                     # data=json.dumps({"Channel": channel})
                     )

            # The volume to dispense is set according to the setting in the head of the function (in mL)
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                'function_identifier': 'SetVolume',
                                'parameters': [channel, volume[i]]}
                 # data=json.dumps({"Channel": channel,
                 #      "Volume": volume[i]
                 #      })
            )

            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                'function_identifier': 'SetFlowRate',
                                'parameters': [channel, flow_rate[i]]}
                 #data=json.dumps({"Channel": channel,
                 #      "SetFlowRate": flow_rate[i]
                 #      })
                 )

            # Gets the current direction direction of the channel and compares to the desired setting. If the settings
            # do not match, the sets it to counter-clockwise ...
            pump_direction = \
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                'function_identifier': 'GetPumpDirection', 'response_identifiers': "PumpDirection",
                                'parameters': [channel]}
                 # data=json.dumps({"Channel": channel})
                 ).json()['response']['PumpDirection']
            if pump_direction != direction[i] and direction[i] == 'K':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                    'function_identifier': 'SetDirectionCounterClockwise',
                                    'parameters': [channel]}
                     #data=json.dumps({"Channel": channel}
                     #)
                     )
            # ... or clockwise rotation direction

            elif pump_direction != direction[i] and direction[i] == 'J':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                    'function_identifier': 'SetDirectionClockwise',
                                    'parameters': [channel]}
                     # data=json.dumps({"Channel": channel})
                    )

        start_time = time()  # Notes the time
        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                'function_identifier': 'StartPump',
                                'parameters': [channel]}
                 # data=json.dumps({"Channel": channel})
                 )
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
        self.enable_channel_addressing()

        # checks, whether flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            is_at_flow_rate_mode = post(route, params={'service_uuid': self.pump['uuid'],
                                                       'feature_identifier': 'ParameterController',
                                                       'function_identifier': 'GetFlowRateAtModes',
                                                       'response_identifiers': "CurrentFlowRate",
                                                       'parameters': [channel]}
                                        #data=json.dumps({"Channel": channel})
                                        ).json()['response']['CurrentFlowRate']
            if is_at_flow_rate_mode is False:
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                    'function_identifier': 'SetFlowRateMode'},
                     data=json.dumps({"Channel": channel})
                     )

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                max_flow_rate_with_cal = post(route, params={'service_uuid': self.pump['uuid'],
                                                             'feature_identifier': 'ParameterController',
                                                             'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                             'response_identifiers': "MaximumFlowRateWithCalibration",
                                                             'parameters': [channel]}
                                              #data=json.dumps({"Channel": channel})
                                              ).json()['response']['MaximumFlowRateWithCalibration']
                flow_rate.append(max_flow_rate_with_cal)
            logging.info('Calibrated maximum flow rate used: ', flow_rate)

        # Iteration: for each channel following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Time mode, with allows to dispense for a set time duration with a set flow rate
            current_pump_mode = post(route,
                                     params={'service_uuid': self.pump['uuid'],
                                             'feature_identifier': 'ParameterController',
                                             'function_identifier': 'GetMode',
                                             'response_identifiers': "CurrentPumpMode",
                                             'parameters': [channel]}
                                     #data=json.dumps({"Channel": channel})
                                     ).json()['response'][
                'CurrentPumpMode']
            if current_pump_mode != 'N':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                    'function_identifier': 'SetTimeMode',
                                    'parameters': [channel]}
                     #data=json.dumps({"Channel": channel})
                     )

            # The time duration to dispense is set according to the setting in the head of the function (in seconds with
            # max. 1 decimal place)
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                'function_identifier': 'SetCurrentRunTime',
                                'parameters': [channel, runtime[i]]}
                 #data=json.dumps({"Channel": channel,
                 #      "RunTime": runtime[i]})
                 )
            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                'function_identifier': 'SetFlowRate',
                                'parameters': [channel, flow_rate[i]]}
                 #data=json.dumps({"Channel": channel,
                 #      "SetFlowRate": flow_rate[i]})
            )
            # Gets the current rotation direction of the channel and compares to the desired setting. If the settings do
            # not match, the sets it to counter-clockwise ...
            pump_direction = \
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                'function_identifier': 'GetPumpDirection', 'response_identifiers': "PumpDirection",
                                'parameters': [channel]}
                 #data=json.dumps({"Channel": channel})
                 ).json()['response']['PumpDirection']
            if pump_direction != direction[i] and direction[i] == 'K':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                    'function_identifier': 'SetDirectionCounterClockwise',
                                    'parameters': [channel]}
                     # data=json.dumps({"Channel": channel}))
                     )
            # ... or clockwise rotation direction

            elif pump_direction != direction[i] and direction[i] == 'J':
                post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                    'function_identifier': 'SetDirectionClockwise',
                                    'parameters': [channel]}
                     # data=json.dumps({"Channel": channel})
                     )

        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                'function_identifier': 'StartPump',
                                'parameters': [channel]}
                 # data=json.dumps({"Channel": channel})
                 )
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
        self.enable_channel_addressing()

        for channel in channels:
            post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                'function_identifier': 'StopPump',
                                'parameters': [channel]}
                 # data=json.dumps({"Channel": channel})
                 )
            return_val = f'Channel {channel} stopped \n\n'
        return return_val

    def pump_status(self):
        """
        Method to check whether the pump is currently running (+) or not (-).

        If one or more channels are in use, the status would be 'running'. However, it is impossible to distinguish,
        which and how many channels are used.
        """

        return_val = post(route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                         'function_identifier': 'GetPumpStatus',
                                         'response_identifiers': "CurrentPumpStatus",
                                         'parameters': [ADDRESS]}
                          # data=json.dumps({"Address": ADDRESS})
                          ).json()['response'][
            'CurrentPumpStatus']
        return return_val
