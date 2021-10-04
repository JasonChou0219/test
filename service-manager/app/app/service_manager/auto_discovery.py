from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
import socket
import time
from typing import List

from app.schemas import ServiceCreate


class Listener(ServiceListener):
    def __init__(self):
        self.serversInformation = []

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip = socket.inet_ntoa(info.addresses[0])
        port = info.port
        server_name = info.properties.get(b'server_name')
        if server_name is not None:
            server_name = server_name.decode("utf-8")
        else:
            server_name = 'Unknown'
        server_uuid = name.split('.')[0]
        server_hostname = info.server
        if server_hostname is None:
            server_hostname = 'Unknown'
        self.serversInformation.append(
            (server_name, server_hostname, ip, port, server_uuid))

    def remove_service(self, zeroconf, type, name):
        pass

    def update_service(self, zeroconf, type, name):
        pass


class AutoDiscovery:

    @staticmethod
    def find() -> List[ServiceCreate]:
        """
        Return a list of ServiceCreate objects of which each entry represents the information about a server discovered on the network.
    
        :return: List of SiLa server information
        :rtype: List[SiLaServerInfo]
        """
    
        zeroconf = Zeroconf()
        listener = Listener()
        browser = ServiceBrowser(zeroconf, "_sila._tcp.local.", listener)
    
        time.sleep(1)
    
        zeroconf.close()
        browser.cancel()
        ls = [
            ServiceCreate(name=info[0], hostname=info[1], ip=info[2], port=info[3], service_uuid=info[4])
            for info in listener.serversInformation
        ]
        print(ls)

        zeroconf = Zeroconf()
        listener = Listener()
        browser = ServiceBrowser(zeroconf, "_tcp.local.", listener)

        time.sleep(1)

        zeroconf.close()
        browser.cancel()
        ls = [
            ServiceCreate(name=info[0], hostname=info[1], ip=info[2], port=info[3], service_uuid=info[4])
            for info in listener.serversInformation
        ]
        print(ls)

        return [
            ServiceCreate(name=info[0], hostname=info[1], ip=info[2], port=info[3], service_uuid=info[4])
            for info in listener.serversInformation
        ]

auto_discovery = AutoDiscovery()
