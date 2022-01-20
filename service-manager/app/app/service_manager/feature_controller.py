from multiprocessing.pool import ThreadPool
from typing import List, Dict

from sila2.client import SilaClient

from app.schemas.sila_dto import Feature
from app.service_manager.featurer_parser import FeatureParser


class FeatureController:
    sila_client: SilaClient
    features: Dict[str, Feature]

    def __init__(self, sila_client: SilaClient):
        feature_xml = []
        self.features = {}
        self.sila_client = sila_client

        for feature_identifier in self.sila_client.SiLAService.ImplementedFeatures.get():
            feature_xml.append(feature_identifier)

        feature_definitions_xml = list(
            map(lambda id: self.sila_client.SiLAService.GetFeatureDefinition(id), feature_xml))

        for xml_definition in feature_definitions_xml:
            for x in range(0, len(xml_definition)):
                parser = FeatureParser(xml_definition[x])
                self.features.update(parser.parse_xml())

    def get_feature_by_identifier(self, identifier: str):
        return self.features[identifier]

    def run_function(self,
                     identifier: str,
                     function: str,
                     is_property: bool,
                     is_observable: bool,
                     response_identifiers: List[str] = None,
                     parameters: List = None):
        response = (getattr(vars(self.sila_client)[identifier], function))

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
# TODO reimplement with DB
# def parse_datatype(xml_subtree):


def main():
    client = SilaClient("127.0.0.1", 50052)

    fc = FeatureController(client)

    print(fc.get_feature_by_identifier("TimerProvider"))
    print(fc.run_function("GreetingProvider", "StartYear", True, False))

    """
    pool = ThreadPool()
    # TODO from Threading, Event, Queue?
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
