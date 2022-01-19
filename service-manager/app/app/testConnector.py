from typing import List
from multiprocessing.pool import ThreadPool
from sila2.client import SilaClient
from lxml import etree
from app.schemas.sila_dto import Feature, Command, CommandParameter, DataType, CommandResponse, Property, \
    DefinedExecutionError


def run_function(client: SilaClient,
                 identifier: str,
                 function: str,
                 is_property: bool,
                 is_observable: bool,
                 response_identifiers: List[str] = None,
                 parameters: List = None):
    response = (getattr(vars(client)[identifier], function))

    response_values = []

    if is_property:
        if is_observable:
            # how to cancel
            response_stream = response.subscribe()
            for value in response_stream:
                print(value)

        return response.get()
    else:
        command_response = response(*parameters)
        if is_observable:
            response_stream = command_response.subscribe_intermediate_responses()

            # might need a flip around for user canceling
            while not command_response.done:
                for value in response_stream:
                    print("Value:", value)

            response_stream.cancel()
            command_response = command_response.get_responses()

        for response_id in response_identifiers:
            response_values.append(getattr(command_response, response_id))

    return response_values


# TODO ObservableTest
#TODO reimplement with DB
# def parse_datatype(xml_subtree):


def parse_xml(xml_string):
    root = etree.fromstring(xml_string)

    feature = Feature()
    feature.feature_version = root.get('FeatureVersion')
    feature.sila2_version = root.get('SiLA2Version')
    feature.originator = root.get('Originator')
    feature.maturity_level = root.get('MaturityLevel')
    feature.category = root.get('Category')

    locale_placeholder = root.get('Locale')
    if locale_placeholder:
        feature.locale = locale_placeholder

    feature_commands = []
    feature_props_ls = []
    feature_errors = []

    for feature_property in root.getchildren():
        if 'Identifier' in feature_property.tag:
            feature.identifier = feature_property.text
        if 'DisplayName' in feature_property.tag:
            feature.display_name = feature_property.text
        if 'Description' in feature_property.tag:
            feature.description = feature_property.text
        if 'Command' in feature_property.tag:
            command = Command()
            command_parameter_list = []
            command_response_list = []
            command_error_identifier_list = []

            for command_props in feature_property.getchildren():
                if 'Identifier' in command_props.tag:
                    command.identifier = command_props.text
                if 'DisplayName' in command_props.tag:
                    command.display_name = command_props.text
                if 'Description' in command_props.tag:
                    command.description = command_props.text
                if 'Observable' in command_props.tag:
                    command.observable = False if command_props.text == 'No' else True
                if 'Parameter' in command_props.tag:
                    command_parameter = CommandParameter()

                    for command_params in command_props.getchildren():
                        if 'Identifier' in command_params.tag:
                            command_parameter.identifier = command_params.text
                        if 'DisplayName' in command_params.tag:
                            command_parameter.display_name = command_params.text
                        if 'Description' in command_params.tag:
                            command_parameter.display_name = command_params.text
                        if 'DataType' in command_params.tag:
                            data_type = DataType()

                            for data_type_elems in command_params.getchildren():
                                if 'Basic' in data_type_elems.tag:
                                    data_type.type = data_type_elems.text
                            command_parameter.data_type = data_type

                    command_parameter_list.append(command_parameter)

                if 'Response' in command_props.tag:
                    command_response = CommandResponse()

                    for command_params in command_props.getchildren():
                        if 'Identifier' in command_params.tag:
                            command_response.identifier = command_params.text
                        if 'DisplayName' in command_params.tag:
                            command_response.display_name = command_params.text
                        if 'Description' in command_params.tag:
                            command_response.display_name = command_params.text
                        if 'DataType' in command_params.tag:
                            data_type = DataType()

                            for data_type_elems in command_params.getchildren():
                                if 'Basic' in data_type_elems.tag:
                                    data_type.type = data_type_elems.text
                            command_response.data_type = data_type
                    command_response_list.append(command_response)
                if 'DefinedExecutionErrors' in command_props.tag:
                    for command_error in command_props.getchildren():
                        command_error_identifier_list.append(command_error.text)

            command.parameters = command_parameter_list
            command.responses = command_response_list
            command.error_identifiers = command_error_identifier_list
            feature_commands.append(command)

        if 'Property' in feature_property.tag:
            sila_property = Property()
            for feature_props in feature_property.getchildren():
                if 'Identifier' in feature_props.tag:
                    sila_property.identifier = feature_props.text
                if 'DisplayName' in feature_props.tag:
                    sila_property.display_name = feature_props.text
                if 'Description' in feature_props.tag:
                    sila_property.description = feature_props.text
                if 'Observable' in feature_props.tag:
                    sila_property.observable = False if feature_props.text == 'No' else True

                if 'DataType' in feature_props.tag:
                    data_type = DataType()

                    for data_type_elems in feature_props.getchildren():
                        if 'Basic' in data_type_elems.tag:
                            data_type.type = data_type_elems.text
                    sila_property.data_type = data_type
            feature_props_ls.append(sila_property)

        if 'DefinedExecutionError' in feature_property.tag:
            error = DefinedExecutionError()
            for error_props in feature_property.getchildren():
                if 'Identifier' in error_props.tag:
                    error.identifier = error_props.text
                if 'DisplayName' in error_props.tag:
                    error.display_name = error_props.text
                if 'Description' in error_props.tag:
                    error.description = error_props.text
            feature_errors.append(error)

    feature.commands = feature_commands
    feature.properties = feature_props_ls
    feature.errors = feature_errors

    return feature


def main():
    client = SilaClient("127.0.0.1", 50052)

    features = []

    for feature_identifier in client.SiLAService.ImplementedFeatures.get():
        features.append(feature_identifier)

    feature_definitions = list(map(lambda id: client.SiLAService.GetFeatureDefinition(id), features))

    print(feature_definitions[3][0])

    my_features = []

    for definition in feature_definitions:
        for x in range(0, len(definition)):
            my_features.append(str(parse_xml(definition[x])))

    pool = ThreadPool()
    #TODO from Threading, Event, Queue?
    timer = pool.apply_async(run_function, (client, 'TimerProvider', 'Countdown', False, True,
                                            ["Timestamp"], [10, "Hello SILA"]))
    greeting = pool.apply_async(run_function, (client, "GreetingProvider", "SayHello", False, False,
                                               ["Greeting"], ["World"]))
    start_year = pool.apply_async(run_function, (client, "GreetingProvider", "StartYear", True, False))

    current_day_time = pool.apply_async(run_function, (client, "TimerProvider", "CurrentTime", True, False))

    current_day_time_sub = pool.apply_async(run_function, (client, "TimerProvider", "CurrentTime", True, True))

    print(f"Server says '{greeting.get()[0]}' and was started in the year {start_year.get()}")

    print(f"Server finished at {timer.get()}")

    print(f"Current DayTime {current_day_time.get()}")




"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(run_function, client, 'TimerProvider', 'Countdown', False, True,
                                 ["Timestamp"], [1000000, "Hello SILA"]),
        run_function(client, "GreetingProvider", "SayHello", False, False, ["Greeting"], ["World"]),
        run_function(client, "GreetingProvider", "StartYear", True, False)]

        timestamp = future[0].result()
        greeting = future[1]
        start_year = future[2]
"""

if __name__ == "__main__":
    main()
