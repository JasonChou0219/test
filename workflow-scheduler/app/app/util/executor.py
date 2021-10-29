import docker
import logging
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Executor():
    def __init__(self):
        self.client = docker.from_env()


    def run(self):
        # run new container from image
        # container = self.client.containers.run('zechlin/node-red-executor', detach=True, network='sila2_manager_default', ports={'1880/tcp': 2880}, hostname="test", name="test")
        # container = self.client.containers.run('zechlin/node-red-executor', detach=True, network='sila2_manager_default', ports={1880:1880})
        # print(container.name)
        # print("----")
        # r = requests.get("http://workflow-designer:1880/flows")

        n = self.client.networks.list(names=["sila2_manager_default"], greedy=True)
        # n[0].connect(container.id)
        # n[0].reload()
        for x in n[0].containers:
            print(x.name)
        # time.sleep(10)
        # try:
        # s = requests.get(f'http://{container.name}:1880/flows')
        s = requests.get('http://172.18.0.17:1880/flows')
        # s = requests.get('http://exciting_blackwell:1880/flows')
        print(s.json())
        # except:
        #     pass

        # container.remove(force=True)
        print("END")

    def __push_workflow_to_container(self, workflow, container):
        pass

