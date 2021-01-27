import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from source.device_manager.sila_auto_discovery.sila_auto_discovery import find


servers = find()
