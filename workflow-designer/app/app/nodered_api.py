import requests
import json
from classes_proto import Flow


def get_flows(node_red_address: str):
    r = requests.get(f'{node_red_address}/flows')
    r_decoded = r.json()
    return r_decoded


def get_flow(node_red_address: str, flow_id) -> Flow:
    r = requests.get(f'{node_red_address}/flow/{flow_id}')
    r_decoded = r.json()
    flow = Flow.parse_obj(r_decoded)
    flow.data = r_decoded
    return flow


def post_flow(node_red_address: str, flow: Flow):
    data = flow.data
    r = requests.post(f'{node_red_address}/flow', json=data)
    print(r.raise_for_status())


def post_flow_by_id(source_node_red_address: str, target_node_red_address: str, flow_id: str):
    f = get_flow(source_node_red_address, flow_id)
    post_flow(target_node_red_address, f)
