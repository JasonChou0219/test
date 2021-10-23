import nodered_api as nr_api
import database

_node_red_editor_address = 'http://127.0.0.1:1880'
_node_red_exec_address = 'http://127.0.0.1:1337'


if __name__ == '__main__':
    flow = database.get_flows()
    print(flow)
    nr_api.post_flows(_node_red_exec_address, flow)
    pass
