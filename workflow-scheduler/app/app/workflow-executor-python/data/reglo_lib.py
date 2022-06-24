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


class Pump:
    """Volume at Rate mode and Time at Rate mode"""

    def __init__(self, pump: dict, address: int, route: str):
        self.pump = pump
        self.address = address
        self.route = route
        self.enable_channel_addressing()

    def enable_channel_addressing(self):
        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on). If it is already enabled, then the command is skipped
        is_channel_addressing = post(self.route,
                                     params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                             'function_identifier': 'GetChannelAddressing',
                                             'response_identifiers': "ChannelAddressing"},
                                     json={"Address": self.address}
                                     ).json()['response']['ChannelAddressing']
        if is_channel_addressing is False:
            post(self.route,
                 params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                         'function_identifier': 'SetChannelAddressing'},
                 json={"Address": self.address, "ChannelAddressing": True}
                 )

    def adjust_pump_settings(self):
        self.enable_channel_addressing()
        is_event_messages = post(self.route,
                                 params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                         'function_identifier': 'GetEventMessages',
                                         'response_identifiers': "EventMessages"},
                                 json={"Address": self.address}
                                 ).json()['response']['EventMessages']
        if is_event_messages:
            # event_messages_set = pump_client.DeviceService.SetEventMessages(Address=1,
            #                                                                 EventMessages=False).EventMessagesSet
            event_messages_set = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                          'feature_identifier': 'DeviceService',
                                                          'function_identifier': 'SetEventMessages',
                                                          'response_identifiers': "EventMessagesSet"},
                                      json={"Address": self.address, "EventMessages": False}
                                      ).json()['response']['EventMessagesSet']
            print(f'Event messages are enabled. Disabled event messages: {event_messages_set}')
            is_event_messages = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                         'feature_identifier': 'DeviceService',
                                                         'function_identifier': 'GetEventMessages',
                                                         'response_identifiers': "EventMessages"},
                                     json={"Address": self.address}
                                     ).json()['response']['EventMessages']
            print(f'{"Event messages disabled" if not is_event_messages else "Event messages not disabled!"}')

    def pump_set_volume_at_flow_rate(self, flow_rate=None, channels=[1, 2], volume=[80, 80], direction=['K', 'K']):
        """
        Method to dispense a set volume (mL, max 2 decimal places, in a list []) with a set flow rate (mL/min, max 2
        decimal places, in a list []), rotation direction (J=clockwise, K=counter-clockwise, in a list []) for specific
        channel or channels.
        Pump address for Reglo ICC is set on 1, yet can be changed with SetPumpAddress function

        If several channels are used, there must be same number of values in each other parameter, except for pump
        and return_val.
        """
        msg = ''
        start_time0 = time()
        self.enable_channel_addressing()

        # Checks whether the flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            flow_rate_at_mode = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                         'feature_identifier': 'ParameterController',
                                                         'function_identifier': 'GetFlowRateAtModes',
                                                         'response_identifiers': "CurrentFlowRate"},
                                     json={"Channel": channel}
                                     ).json()['response']['CurrentFlowRate']
            print(f'Flow rate at mode is: {flow_rate_at_mode}')
            flow_rate_at_mode = False
            if flow_rate_at_mode is False:
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                         'function_identifier': 'SetFlowRateMode'},
                     json={"Channel": channel}
                     )

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                print('Channel is', channel, flush=True)
                max_flow_rate_with_cal = post(self.route,
                                              params={'service_uuid': self.pump['uuid'],
                                                      'feature_identifier': 'ParameterController',
                                                      'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                      'response_identifiers': "MaximumFlowRateWithCalibration"},
                                              json={"Channel": channel}
                                              ).json()['response']['MaximumFlowRateWithCalibration']
                print(f'Max flow rate with calibration is: {max_flow_rate_with_cal}', flush=True)
                flow_rate.append(max_flow_rate_with_cal)
            logging.info('Calibrated maximum flow rate used: ', flow_rate)

        # Iteration: for each channel the following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Volume at Rate mode, which allows to dispense a set volume with a set flow rate
            current_pump_mode = post(self.route,
                                     params={'service_uuid': self.pump['uuid'],
                                             'feature_identifier': 'ParameterController',
                                             'function_identifier': 'GetMode',
                                             'response_identifiers': "CurrentPumpMode"},
                                     json={"Channel": channel}
                                     ).json()['response']['CurrentPumpMode']
            print(f'Current pump mode is: {current_pump_mode}', flush=True)
            if current_pump_mode != 'O':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                         'function_identifier': 'SetVolumeRateMode'},
                     json={"Channel": channel}
                     )
            # The volume to dispense is set according to the setting in the head of the function (in mL)
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                     'function_identifier': 'SetVolume'},
                 json={"Channel": channel, "Volume": volume[i]}
                 )
            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                     'function_identifier': 'SetFlowRate'},
                 json={"Channel": channel, "SetFlowRate": flow_rate[i]}
                 )
            # Gets the current direction direction of the channel and compares to the desired setting. If the settings
            # do not match, the sets it to counter-clockwise ...
            pump_direction = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                      'feature_identifier': 'DriveController',
                                                      'function_identifier': 'GetPumpDirection',
                                                      'response_identifiers': "PumpDirection"},
                                  json={"Channel": channel}
                                  ).json()['response']['PumpDirection']
            logging.info(f'Pump direction is: {pump_direction}')
            if pump_direction != direction[i] and direction[i] == 'K':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                         'function_identifier': 'SetDirectionCounterClockwise'},
                     json={"Channel": channel}
                     )
                logging.info(f'Set pump direction to CounterClockwise: K')
            # ... or clockwise rotation direction

            elif pump_direction != direction[i] and direction[i] == 'J':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                         'function_identifier': 'SetDirectionClockwise'},
                     json={"Channel": channel}
                     )
                logging.info(f'Set pump direction to Clockwise: J')

        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                     'function_identifier': 'StartPump'},
                 json={"Channel": channel}
                 )
            msg = f'Volume at Rate mode on channel {channel} for volume {volume[i]} mL at rate {flow_rate[i]} ' \
                         f'mL/min set \n'
        # logging.info('--- Total execution time: %s seconds ---' %((time.time()-start_time0)))

        # calculate maximum pump duration
        pump_duration = []
        for i, v in enumerate(volume):
            pump_duration.append(v/flow_rate[i])
        return msg, pump_duration

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
        msg = ''

        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        self.enable_channel_addressing()

        # checks, whether flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            is_at_flow_rate_mode = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                            'feature_identifier': 'ParameterController',
                                                            'function_identifier': 'GetFlowRateAtModes',
                                                            'response_identifiers': "CurrentFlowRate"},
                                        json={"Channel": channel}
                                        ).json()['response']['CurrentFlowRate']
            logging.info(f'Pump is at flow rate mode: {is_at_flow_rate_mode}')
            if is_at_flow_rate_mode is False:

                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                         'function_identifier': 'SetFlowRateMode'},
                     json={"Channel": channel}
                     )
                logging.info(f'Pump switched to flow rate mode!')

        # If flow rate was not defined, max calibrated values are used
        if flow_rate is None:
            flow_rate = []
            for i, channel in enumerate(channels):
                max_flow_rate_with_cal = post(self.route,
                                              params={'service_uuid': self.pump['uuid'],
                                                      'feature_identifier': 'ParameterController',
                                                      'function_identifier': 'GetMaximumFlowRateWithCalibration',
                                                      'response_identifiers': "MaximumFlowRateWithCalibration"},
                                              json={"Channel": channel}
                                              ).json()['response']['MaximumFlowRateWithCalibration']
                flow_rate.append(max_flow_rate_with_cal)
            logging.info('Calibrated maximum flow rate used: ', flow_rate)

        # Iteration: for each channel following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Time mode, with allows to dispense for a set time duration with a set flow rate
            current_pump_mode = post(self.route,
                                     params={'service_uuid': self.pump['uuid'],
                                             'feature_identifier': 'ParameterController',
                                             'function_identifier': 'GetMode',
                                             'response_identifiers': "CurrentPumpMode"},
                                     json={"Channel": channel}
                                     ).json()['response']['CurrentPumpMode']
            logging.info('Current pump mode is: ', current_pump_mode)
            current_pump_mode = 'O'
            if current_pump_mode != 'N':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                         'function_identifier': 'SetTimeMode'},
                     json={"Channel": channel}
                     )
                logging.info('Pump mode not "N". Switching pump mode!')
            # The time duration to dispense is set according to the setting in the head of the function (in seconds with
            # max. 1 decimal place)
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                     'function_identifier': 'SetCurrentRunTime'},
                 json={"Channel": channel, "RunTime": runtime[i]}
            )
            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'ParameterController',
                                     'function_identifier': 'SetFlowRate'},
                 json={"Channel": channel, "SetFlowRate": flow_rate[i]}
            )
            # Gets the current rotation direction of the channel and compares to the desired setting. If the settings do
            # not match, the sets it to counter-clockwise ...
            pump_direction = post(self.route, params={'service_uuid': self.pump['uuid'],
                                                      'feature_identifier': 'DriveController',
                                                      'function_identifier': 'GetPumpDirection',
                                                      'response_identifiers': "PumpDirection"},
                                  json={"Channel": channel}
                                  ).json()['response']['PumpDirection']
            logging.info(f'Pump direction is: {pump_direction}')
            if pump_direction != direction[i] and direction[i] == 'K':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                         'function_identifier': 'SetDirectionCounterClockwise'},
                     json={"Channel": channel}
                     )
                logging.info(f'Set pump direction to CounterClockwise: K')
            # ... or clockwise rotation direction

            elif pump_direction != direction[i] and direction[i] == 'J':
                post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                         'function_identifier': 'SetDirectionClockwise'},
                     json={"Channel": channel}
                     )
                logging.info(f'Set pump direction to Clockwise: J')

        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                     'function_identifier': 'StartPump'},
                 json={"Channel": channel}
                 )
            msg = f'Time mode on channel {channel} for time {runtime[i]} seconds at rate {flow_rate[i]} ' \
                  f'mL/min set \n\n'
            logging.info(msg)

        return msg, [float(t) for t in runtime]

    def pump_stop(self, channels=[1, 2]):
        """
        Method to stop the channel(s).
        """
        msg = ''
        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        self.enable_channel_addressing()

        for channel in channels:
            post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DriveController',
                                     'function_identifier': 'StopPump'},
                 json={"Channel": channel}
                 )
            msg = f'Channel {channel} stopped \n\n'
            logging.info(msg)
        return msg

    def pump_status(self):
        """
        Method to check whether the pump is currently running (+) or not (-).

        If one or more channels are in use, the status would be 'running'. However, it is impossible to distinguish,
        which and how many channels are used.
        """

        return_val = post(self.route, params={'service_uuid': self.pump['uuid'], 'feature_identifier': 'DeviceService',
                                              'function_identifier': 'GetPumpStatus',
                                              'response_identifiers': "CurrentPumpStatus"},
                          json={"Address": self.address}
                          ).json()['response']['CurrentPumpStatus']
        logging.info(return_val)
        return return_val
