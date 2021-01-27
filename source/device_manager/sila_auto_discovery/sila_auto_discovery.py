from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
import socket
import time
from dataclasses import dataclass
from typing import List


@dataclass
class SilaServerInfo:
    """ Stores SiLA device information displayed by the server in the network via mDNS """
    uuid: str
    name: str
    ip: str
    port: int
    hostname: str


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
            (server_uuid, server_name, ip, port, server_hostname))

    def remove_service(self, zeroconf, type, name):
        pass

    def update_service(self, zeroconf, type, name):
        pass


def find() -> List[SilaServerInfo]:
    """
    Return a list of SilaServerInfo where each entry represents the information about a server discovered on the network

    :return: list of SilaServerInfo
    :rtype: List[SiLaServerInfo]
    """

    zeroconf = Zeroconf()
    listener = Listener()
    browser = ServiceBrowser(zeroconf, "_sila._tcp.local.", listener)

    time.sleep(1)

    zeroconf.close()
    browser.cancel()

    return [
        SilaServerInfo(info[0], info[1], info[2], info[3], info[4])
        for info in listener.serversInformation
    ]
