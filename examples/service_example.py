# This example will show you how to import a service client
import time


def run(services):
    """ Instantiates selected services for this experiment """

    # Check which services are available
    print(f'{time.time()}: Imported services: {[service.name for service in services]}', flush=True)

    # Assign device
    client = services[0]
    print(f'Client is: {client} and of type {type(client)}', flush=True)

    # Make a property call
    response = client.call_property("SiLAService", "ServerName")
    print(f'Response is: {response}', flush=True)

# ...
# yourObject = devices['HelloSiLA_server']()
# You can call functions as described for every command and property in the service feature explorer under "Usage"
# To call the property "StartYear" of the HelloSiLA example service use:
# StartYear = yourObject.call_property("GreetingProvider","StartYear")

# To run the "SayHello" command use:
# response = yourObject.call_command("GreetingProvider","SayHello",parameters={"Name": 'some name'})

# Note: you need to replace the "yourObject" part of the command with the client object of that service!
