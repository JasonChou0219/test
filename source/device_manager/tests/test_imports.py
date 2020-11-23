import unittest
import os


class TestImports(unittest.TestCase):

    def test_imports(self):
        self.assertTrue(os.path.exists("source/device_manager/command-line-interface/parser.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/data_handler.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/device_feature.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/device_info.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/device_interface.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/dynamic_client.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/sila_device.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_layer/sila_feature.py"))
        self.assertTrue(os.path.exists("source/device_manager/hosts/hosts.py"))
        self.assertTrue(os.path.exists("source/device_manager/sila_auto_discovery/sila_auto_discovery.py"))
        self.assertTrue(os.path.exists("source/device_manager/data_directories.py"))
        self.assertTrue(os.path.exists("source/device_manager/database.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_log.py"))
        self.assertTrue(os.path.exists("source/device_manager/device_manager.py"))
        self.assertTrue(os.path.exists("source/device_manager/sila_server.py"))
        self.assertTrue(os.path.exists("source/device_manager/thread_local_storage.py"))
        self.assertTrue(os.path.exists("source/device_manager/user.py"))
        self.assertTrue(os.path.exists("source/backend/device_manager_service.py"))
