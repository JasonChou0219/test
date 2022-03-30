from queue import Queue
import docker
from docker.models.containers import Container

log_dict = {}


def get_queue_item(q: Queue):
    i = q.get()
    q.task_done()
    return i


if __name__ == '__main__':
    client = docker.from_env()
    container = client.containers.create("python:3")
    q = log_dict[container.id] = Queue()
    print(log_dict[container.id])
    container.remove()

