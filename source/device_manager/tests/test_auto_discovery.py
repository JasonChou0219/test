import unittest
from sila2lib.sila_server import SiLA2Server
import threading
from os import path

import socket

from source.device_manager.sila_auto_discovery import sila_auto_discovery
from source.device_manager.device_layer.dynamic_client import DynamicSiLA2Client
from source.device_manager.device_layer.sila_device import SilaDevice
from source.device_manager.sila_auto_discovery.sila_auto_discovery import SilaServerInfo
from source.device_manager.data_directories import TEMP_DIRECTORY


class TestAutoDiscovery(unittest.TestCase):

    server_name = "testServer"
    server_ip = "127.0.0.1"
    server_port = 50051

    @classmethod
    def setUpClass(cls):
        cls.sila_test_server = SiLA2Server(name=cls.server_name,
                                           ip=cls.server_ip,
                                           port=cls.server_port)
        cls.server_uuid = cls.sila_test_server.server_uuid
        cls.server_thread = threading.Thread(target=cls.sila_test_server.run)
        # Daemon threads automatically shut down when the main process exits
        cls.server_thread.setDaemon(True)
        cls.server_thread.start()
        cls.servers_found = sila_auto_discovery.find()
        cls.expected_sila_server_information = SilaServerInfo(
            cls.server_uuid, cls.server_name, cls.server_ip, cls.server_port,
            f"{socket.getfqdn()}.local.")

    def test_discovery_return_parameters(self):
        self.assertTrue(
            self.expected_sila_server_information in self.servers_found)

    def test_client_connection_unencrypted(self):
        index_of_server = self.servers_found.index(
            self.expected_sila_server_information)
        client = DynamicSiLA2Client(
            name="client",
            server_ip=self.servers_found[index_of_server].ip,
            server_port=self.servers_found[index_of_server].port)

    def test_sila_device_and_file_creator(self):
        device1 = SilaDevice(self.server_ip, self.server_port, self.server_uuid,
                             self.server_name)
        self.assertEqual(device1.name, self.server_name)
        self.assertEqual(device1.uuid, self.sila_test_server.server_uuid)
        self.assertIsNotNone(device1.get_feature_names())
        f = open(
            path.join(TEMP_DIRECTORY, 'Sila', device1.uuid, '.server_name'))
        self.assertEqual(f.read(), device1.name)


if __name__ == '__main__':
    unittest.main()
