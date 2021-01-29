import devices

# WIP
# This example will show you how to import a device client
# This is work in progress

# ...
yourObject = devices['HelloSiLA_server']()
# You can call functions as described for every command and property in the device feature explorer under "Usage"
# To call the property "StartYear" of the HelloSiLA example device use:
StartYear = yourObject.call_property("GreetingProvider","StartYear")

# To run the "SayHello" command use:
response = yourObject.call_command("GreetingProvider","SayHello",parameters={"Name": 'some name'})

# Note: you need to replace the "yourObject" part of the command with the client object of that device!