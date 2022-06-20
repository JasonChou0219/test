from time import sleep
from datetime import datetime
print("Finished imports", flush=True)


def run():
    print("Starting workflow", flush=True)
    for i in range(0, 20, 1):
        print(f'Current timestamp: {datetime.now()}', flush=True)
        sleep(2)