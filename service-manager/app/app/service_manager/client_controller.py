from multiprocessing.pool import ThreadPool
from typing import List, Dict

from sila2.client import SilaClient

from app.schemas.sila_dto import Feature


def get_connection_identifier(client_ip: str, client_port: int):
    return client_ip + ":" + str(client_port)

class ClientController:
    silaClients: Dict[str,SilaClient]

    def discover_client(self):
        pass

    def add_client(self, client_ip: str, client_port):
        client_identififer = get_connection_identifier(client_ip, client_port)
        client = SilaClient("127.0.0.1", 50052)
        self.silaClients.update({client_identififer: SilaClient})




client_controller = ClientController()
