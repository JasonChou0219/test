from sila2.client import SilaClient


def main():
    client = SilaClient("172.18.96.239", 50400)

    print(client.SiLAService.ServerDescription.get())
    print(client.SiLAService.ServerName.get())
    for feature_identifier in client.SiLAService.ImplementedFeatures.get():
        print("-", feature_identifier)

    print("-------------------------------------------------------------------")

if __name__ == "__main__":
    main()