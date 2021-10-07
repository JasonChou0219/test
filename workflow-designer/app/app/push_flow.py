import nodered_api as NR_api

_node_red_editor_address = 'http://127.0.0.1:1880'
_node_red_exec_address = 'http://127.0.0.1:1337'


if __name__ == '__main__':
    NR_api.post_flow_by_id(_node_red_editor_address, _node_red_exec_address, 'b90eb00e96c20763')
