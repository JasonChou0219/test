# import websocket
from typing import List, Optional, Union, Dict, Any
from fastapi import WebSocket

from queue import Queue


observables_dict: Dict = {}


async def register_observable(execution_uuid: str):
    observables_dict.update({execution_uuid: Queue(maxsize=1000)})
