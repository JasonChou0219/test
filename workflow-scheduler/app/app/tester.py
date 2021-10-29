from app.util.executor import Executor



def test() -> None:
    ex = Executor()
    ex.start_container()


if __name__ == '__main__':

    test()