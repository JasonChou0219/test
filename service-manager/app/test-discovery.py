from sila2.discovery import SilaDiscoveryBrowser

import logging

def main():
    try:

        print("Starting SiLA Discovery...")
        client = SilaDiscoveryBrowser().find_server(timeout=25)

        if client:
            print("Found", client)

        print("Discovered SiLA Server with the following features:")
        print(client.SiLAService.ServerDescription.get())
        print(client.SiLAService.ServerName.get())
        for feature_identifier in client.SiLAService.ImplementedFeatures.get():
            print("-", feature_identifier)

    except TimeoutError:
        print("Failed to discover SiLA Server")
    except Exception:
        print("Something went wrong")

if __name__ == "__main__":
    main()
