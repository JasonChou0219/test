from app.util.docker_helper import Executor
from datetime import date, datetime


def bla() -> None:
    ex = Executor()
    ex.start_container()

def bla2():
    print(datetime.now())

if __name__ == '__main__':
    bla()