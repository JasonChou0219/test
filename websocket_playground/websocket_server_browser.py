#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import threading, queue

mock_observable_command_payloads_list = [
    # "observable_command_uuid": "The response",
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Intermediate_Response': '123'}),
    ('b841e028-3335-4144-8569-7a1c563bd9f0', {'Intermediate_Response': 'abc'}),
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Intermediate_Response': '456'}),
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Intermediate_Response': '789'}),
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Intermediate_Response': '000'}),
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Response': '101112'}),
    ('fd4082f6-51e6-448b-9882-64a00c117c2f', {'Intermediate_Response': '000'}),
]

# observable_command_payload_queue = queue.Queue()
# for item in mock_observable_command_payloads_list:
#     observable_command_payload_queue.put(item)


def get_execution_uuid(list_entry):
    return list_entry[0]


async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


async def subscribe_command_execution_uuid(websocket, path):
    # This must be implemented with queues and events. This is not functional, but shows how it could work.
    query = await websocket.recv()
    execution_id_response_list = []
    for item in mock_observable_command_payloads_list:
        if item[0] == query:
            execution_id_response_list.append(item[1])
    while True:
        for response in execution_id_response_list:
            if 'Response' in response.keys():
                print(f'Transmitting response: {response}')
                # await websocket.send(response.popitem()[1])
                await websocket.send(list(response.values())[0])
                # await asyncio.sleep(random.random() * 0.1)
                print('Cancel subscription')
                return
            else:
                print(f'Transmitting response: {response}')
                # await websocket.send(response.popitem()[1])
                await websocket.send(list(response.values())[0])
                # await asyncio.sleep(random.random() * 0.1)



# start_server = websockets.serve(time, '127.0.0.1', 5678)
start_server = websockets.serve(subscribe_command_execution_uuid, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
