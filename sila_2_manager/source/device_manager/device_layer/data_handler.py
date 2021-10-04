from influxdb import InfluxDBClient
from source.device_manager.device_layer.sila_device import SilaDevice
from source.device_manager.device_layer.device_interface import DeviceInterface
from typing import List, Dict
import threading, time
import json
from threading import Thread


class DataHandler:
    def __init__(self,
                 host: str,
                 port: int,
                 user: str = 'root',
                 password: str = 'root',
                 dbname: str = 'example'):
        """initialize the data handler  
        Args:
            host : the host of the InfluxDBClient
            port : port of the InfluxDB
            user : username of InfluxDB
            password : password of InfluxDB
            dbname : database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.client = InfluxDBClient(self.host, self.port, self.user, self.password,
                                     self.dbname)
        self.client.create_database(self.dbname)


    def setup(self,get_devices: List[DeviceInterface]):
        interval10=interval50=interval100=[]
        for device in get_devices:
            interval10.append([k for k,v in device.properties_interval.items() if v == 10])
            interval50.append([k for k,v in device.properties_interval.items() if v == 50])
            interval100.append([k for k,v in device.properties_interval.items() if v == 100])
        process = Thread(target=self.run, args=[get_devices, interval10, 10])
        process.start()
        process2 = Thread(target=self.run, args=[get_devices, interval50, 50])
        process2.start()
        process3 = Thread(target=self.run, args=[get_devices, interval100, 100])
        process3.start()

    
    def run(self,get_devices: List[DeviceInterface] , interval_list, interval):
        """Will store all the data of all available device to the time series database
        Args:https://discord.com/channels/709354436090396712/714844196300783626
            get_devices: List of Devices
            interval_list: List of property that we want to run at specific interval
            interval: the interval time between every store to the database
        """
        data = {}
        for device in get_devices:
            if device.get_status == "running":
                # if(device.type=="Sila")
                for features in device.get_feature_names():
                    for property in device.get_properties(features):
                        if property in interval_list:
                            data['measurement'] = property
                            data['tags'] = {'device': device, 'features': features}
                            data['time'] = time.time()
                            data['fields'] = {'value': device.call_property(features, property)}
                            json_body = json.dumps(data)
                            self.client.write_points(json_body)
        threading.Timer(interval, self.run, [get_devices, interval_list, interval]).start()

    @staticmethod
    def get_logs(device):
        """Returns the specified device latest log message
        Args:
            device : The Sila device that we want to get the log for
        Returns:
            list containing LogLevel,time and the massage
        """
        sila = SilaDevice(device.ip, device.port, device.uuid, device.name)
        return sila.call_property('DeviceController', 'GetLog_Result')
