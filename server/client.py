from multiprocessing import Process

from src.src.requests_module import Requester
from server.app import run_server
from server.base import ServerInfo


class Logic:
    pass


if __name__ == '__main__':
    import datetime

    process = Process(target=run_server)
    process.start()

    requester = Requester('http://127.0.0.1:5000', ServerInfo())
    print(requester.get_users(datetime.datetime))

