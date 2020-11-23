import argparse
from source.device_manager.device_manager import DeviceManager,DeviceInfo,datetime

parser = argparse.ArgumentParser(description='A command line interface for the device manager functionality')
parser.add_argument('-a','--get_devices_info',help='Returns a list of devices information from the database', action="store_true")
parser.add_argument('-b','--get_device_info',help='Returns the specified device information from the database(UUID required)', action="store_true")
parser.add_argument('-c','--get_device_instance',help='Returns the specified device instance(UUID required)', action="store_true")
parser.add_argument('-d','--set_device',help='Updates a device in the database', action="store_true")
parser.add_argument('-e','--add_device',help='Add a new device to the database', action="store_true")
parser.add_argument('-f','--delete_device',help='Delete a device from the database', action="store_true")
parser.add_argument('-g','--get_status',help='Get the current status of the specified device', action="store_true")
parser.add_argument('-l','--get_features',help='Get the description of supported features of the specified device', action="store_true")
parser.add_argument('-i','--discover_sila_devices',help='Triggers the sila autodiscovery,Returns the list of discovered devices', action="store_true")
parser.add_argument('-j','--get_log',help='Get log entries from database', action="store_true")







device=DeviceManager()
args = parser.parse_args()
if args.get_devices_info:
    print(device.get_device_info_list())
if args.get_device_info:
    uuid = input("Enter the device UUID : ")
    print(device.get_device_info(uuid))
if args.get_device_instance:
    uuid = input("Enter the device UUID : ")
    print(device.get_device_instance(uuid))
if args.set_device:
    uuid = input("Enter the device UUID : ")
    name = input("Enter the device name : ")
    type = input("Enter the device type : ")
    address = input("Enter the device address : ")
    port = input("Enter the device port : ")
    new_device=DeviceInfo(uuid,name,type,str(address),int(port))
    device.set_device(new_device)
    print(new_device+" was updated")
if args.add_device:
    uuid = input("Enter the device UUID : ")
    name = input("Enter the device name : ")
    type = input("Enter the device type : ")
    address = input("Enter the device address : ")
    port = input("Enter the device port : ")
    new_device=DeviceInfo(uuid,name,type,str(address),int(port))
    device.add_device(new_device)
    print(new_device+" was added")
if args.delete_device:
    uuid = input("Enter the device UUID : ")
    device.delete_device(uuid)
    print("device with UUID: "+ uuid +" was deleted")
if args.get_status:
    uuid = input("Enter the device UUID : ")
    print(device.get_status(uuid))
if args.get_features:
    uuid = input("Enter the device UUID : ")
    print(device.get_features(uuid))
if args.discover_sila_devices:
    print(device.discover_sila_devices())
if args.get_log:
    from_date = input("Enter the start date(leave empty for defult) : ")
    to_date = input("Enter the end date(leave empty for defult): ")
    if from_date=="":
        from_date=0
    if to_date=="":
        to_date = datetime.now().timestamp()
    print(device.get_log(int(from_date),int(to_date)))