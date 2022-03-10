import requests



if __name__ == '__main__':
    flow = requests.get("http://localhost:84/api/v1/workflow/4")
    print(flow.content)
    # print(requests.get("http://localhost:85/flow-manager/all-flows").content)
    # print(requests.get("http://localhost:85/flow-manager/flow-files/flow/1737bc4de665429e").content)
    # s = requests.post(f'http://localhost:85/flow-manager/flow-files/flow/NewFlow', json=flow)
    # print(s.text)
