# Device Layer 

The device layer is a universal interface for all kinds of laboratory devices. It implements all core attributes and functions needed for device communication, i.e. device name, IP, Port, UUID, client_path, client, availability, reservations, status, device type...etc.

# Device Layer Interfaces
The Device Layer Interface is the base class for all the laboratory devices classes that implement it(Sila device, soft sensor, other).it uses the ABC module that provides the infrastructure for defining abstract base classes. we use the @abstractclassmethod decorators to create the function that needs to be implemented in the subclass.

# Functions

1. __init__ 
the first function is the constructor for the class. it is implemented as abstract class method so every class that inherits the abstract class must have a constructor.

2. call_command
the call command function will send a command to the server to be executed, and since every device will communicate with the server in different ways we must also use the @abstractclassmethod decorators.

3. getter and setter functions
we have multiple functions for getting and sitting particular information about the device like (availability, status, reservation). for getting any of these files you need to pass only the SQLite cursor, however for sitting you need to pass additional values.


# Sila Device
the sila device subclass provid the all neaccery functionalty to use a sila device. on creation of the device the class create a dynacmic client to retrieve all the necessary information of that device from the server. this class will be used by the device manger to create sila devices and mange them throu the interface.to create a device you have to pass the ip,port and the database connection object.on cration the device will be added to the sql database.