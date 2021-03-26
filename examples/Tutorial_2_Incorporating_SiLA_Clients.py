"""
TUTORIAL 2: Incorporating SiLA 2 Clients
---------------------------------------------

This example uses the SiLA Python HelloSiLA_Full example server.
You can download it from the repositroy at https://gitlab.com/SiLA2/sila_python/-/tree/master/examples/HelloSiLA2/HelloSiLA2_Full

To run this example follow these steps:

2.1. Add a SiLA Server to your Services (Ideally the HelloSiLA example from the SiLA Python or Tecan repository)
2.2. Go to the Data Handler tab and deactivate the "Activce" checkmark for the device you want to use
2.3. Set up an experiment with and select this script and the device you want to use
2.4. Hit the run button or wait for the scheduled execution time (You can click on the experiment
    name to get the docker container stdout, i.e the output of your script)

Hint 1: The def run() method is compulsory. The services are passed to it in the same order,
    that you select them in during experiment setup, i.e the order they are displayed in in
    the experiment list entry of you experiment

Hint 2: Use the flush argument when using print statements.

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
    print(response, flush=True)
    # A SET command. A call to the DriveController of the pump. Set speed and start the first channel.
    # client.call_command(feature_id="PumpController\n",
    #                  command_id="SetFlowrate",
    #                  parameters = { "channel/constrained/integer": 1,"flowrate/constrained/real": 20.5}
    #                  )
    # pump.call_command(feature_id="PumpController\n",
    #                  command_id="StartPump",
    #                  parameters = { "channel/constrained/integer": 1}
    #                  )

    #reactor_client.call_command(feature_id="PumpController\n",
    #                    command_id="SetDirectionClockwise",
    #                    parameters = { "channel/constrained/integer": 1}
    #                    )


    for i in range(50):
        response = client.call_property("SiLAService\n", "ServerName")
        print(response, flush=True)
        time.sleep(1)