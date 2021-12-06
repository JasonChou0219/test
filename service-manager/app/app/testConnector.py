from sila2.client import SilaClient


def main():
    client = SilaClient("192.168.2.152", 50052)

    print(client.SiLAService.ServerDescription.get())
    print(client.SiLAService.ServerName.get())
    for feature_identifier in client.SiLAService.ImplementedFeatures.get():
        print("-", feature_identifier)

    print("-------------------------------------------------------------------")

    response = client.GreetingProvider.SayHello("World")

    greeting1 = response.Greeting
    start_year = client.GreetingProvider.StartYear.get()

    print(f"Server says '{greeting1}' and was started in the year {start_year}")


if __name__ == "__main__":
    main()
