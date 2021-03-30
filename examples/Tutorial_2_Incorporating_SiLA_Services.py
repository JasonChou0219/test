"""
TUTORIAL 2: Incorporating SiLA 2 Clients
---------------------------------------------

This example uses the SiLA Python HelloSiLA_Full example server.
You can download it from the repository at https://gitlab.com/SiLA2/sila_python/-/tree/master/examples/HelloSiLA2/HelloSiLA2_Full

To run this example follow these steps:

2.1. Add a SiLA Server to your Services (Ideally the HelloSiLA example from the SiLA Python or Tecan repository)
2.2. Go to the Data Handler tab and deactivate the "Active" checkmark for the device you want to use
2.3. Set up an experiment with and select this script and the device you want to use
2.4. Hit the run button or wait for the scheduled execution time (You can click on the experiment
    name to get the docker container stdout, i.e the output of your script)

Hint 3: The command/property call syntax is displayed in the "Services" tab. It is shown under
    "Usage" on the lowest level of the device tree for every command and property.
"""
import time


def run(services):
    """ Instantiates selected devices for this experiment """
    client = services[0]
    print(f'Service instantiated: {client.name}@{client.ip}:{client.port}', flush=True)
    client.connect()
    # A GET command. A call to the SiLAService feature. Request the server name.
    response = client.call_property("SiLAService\n", "ServerName")
    ServerName = response
    print(response, flush=True)

    for i in range(10):
        response = client.call_property("SiLAService\n", "ServerName")
        print(f'{i}. call:', response, flush=True)
        time.sleep(1.5)

    # A Set command. A call to the SiLAService feature. Change the server name.
    client.call_command("SiLAService\n","SetServerName", parameters={"ServerName/constrained/String": "MyNewName"})
    response = client.call_property("SiLAService\n", "ServerName")
    print('Changed name to: ', response['servername/constrained/string'], flush=True)
    # Change the ServerName back to the original one
    client.call_command("SiLAService\n","SetServerName", parameters={
        "ServerName/constrained/String": ServerName['servername/constrained/string']})
    response = client.call_property("SiLAService\n", "ServerName")
    print('Changed name back to:', response['servername/constrained/string'], flush=True)
