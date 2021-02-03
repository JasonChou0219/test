# WIP
# This example will show you how to import a device client
# This is work in progress

import time


def run(devices):
    """ Instantiates selected devices for this experiment """

    # Check which devices are available
    print(f'{time.time()}: Imported devices: {[device.name for device in devices]}', flush=True)

    # Assign device
    client = devices[0]
    print(f'Client is: {client} and of type {type(client)}', flush=True)

    # Make a property call
    response = client.call_property("SiLAService", "ServerName")
    # response = devices[0].call_property("SiLAService", "ServerName")
    print(f'Response is: {response}', flush=True)

# ...
# yourObject = devices['HelloSiLA_server']()
# You can call functions as described for every command and property in the device feature explorer under "Usage"
# To call the property "StartYear" of the HelloSiLA example device use:
# StartYear = yourObject.call_property("GreetingProvider","StartYear")

# To run the "SayHello" command use:
# response = yourObject.call_command("GreetingProvider","SayHello",parameters={"Name": 'some name'})

# Note: you need to replace the "yourObject" part of the command with the client object of that device!
