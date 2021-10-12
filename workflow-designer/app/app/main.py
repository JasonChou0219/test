import requests
import json
from classes_proto import Flow, Node, SubFlow
import database
import sys
import nodered_api as nr_api
import docker
from threading import Thread, Event

_node_red_editor_address = 'http://127.0.0.1:1880'
_node_red_exec_address = 'http://127.0.0.1:1337'


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def decompose_and_safe(rdecomp):
    for t in rdecomp:
        if t["type"] == "tab":
            flow = Flow.parse_obj(t)
            flow.data = json.dumps(t)
            print(flow)
            database.add_flow(flow)
        elif t["type"] == "subflow":
            subflow = SubFlow.parse_obj(t)
            subflow.data = json.dumps(t)
            print(subflow)
            database.add_subflow(subflow)
        else:
            node = Node.parse_obj(t)
            node.data = json.dumps(t)
            print(node)
            database.add_node(node)


def save_flows():
    flows = nr_api.get_flows(_node_red_editor_address)
    for i in flows:
        f = nr_api.get_flow(_node_red_editor_address, i['id'])
        database.add_update_flow(f)


def main():
    loop = True
    client = docker.from_env()
    container = client.containers.get('workflow-executor')
    for line in container.logs(stream=True):
        print(line.strip())


def main_():
    save_flows()
    nr_api.post_flow(_node_red_exec_address, flow)


def main__():
    r = requests.get('http://127.0.0.1:1880/flows')
    rDecomp = r.json()
    flow = Flow.parse_obj(rDecomp[0])
    res = requests.get(f'http://127.0.0.1:1880/flow/{flow.id}')
    res = res.json()
    print(type(res))
    r = requests.post(f'http://127.0.0.1:1337/flow', json=res)
    print(r.raise_for_status())


if __name__ == '__main__':
    database.add_flows_table()
    # database.add_nodes_table()
    # database.add_subflows_table()

    main()
    sys.exit()

    # run on loop
    # Listen for changes
    # pull flow, update in DB
    # choose flow to push to executor


    r = requests.get('http://127.0.0.1:1880/flows')
    rDecomp = r.json()
    # decompose_and_safe(rDecomp)
    flowID = ""
    # for t in rDecomp:
    #     if t["type"] == "tab":
    flow = Flow.parse_obj(rDecomp[0])
    res = requests.get(f'http://127.0.0.1:1880/flow/{flow.id}')
    res = res.json()

    print(res)
    jprint(res)
    r = requests.post(f'http://127.0.0.1:1337/flow', json=res)
    print(r.raise_for_status())

    flow = Flow.parse_obj(res)
    # flow = Flow.parse_obj.json())
    # flow.data = json.dumps(t)
    flow.data = json.dumps(res)
    database.add_flow(flow)
    flowID = flow.id

    newFlow = database.get_flow(flowID)
    print(newFlow.data)
    msg = json.loads(newFlow.data)
    # r = requests.post(f'http://127.0.0.1:1337/flow', data=msg)
    print(r.raise_for_status())
