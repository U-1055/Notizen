import json

import requests

import datetime

from server.base import ServerInfo


def form_request(server: str, *args) -> str:
    return f'{server}{''.join([f'/{el}' for el in args])}'


class Requester:

    def __init__(self, server: str, addresses: ServerInfo = ServerInfo()):
        self._server = server
        self._addresses = addresses

    def check_authorize(self, user_id: int):
        return requests.get(f'{self._server}/user?user_id={user_id}/data')

    def authorize(self, login: str, password: str):
        return requests.get(f'{self._server}/authorize/{login}/{password}')

    def add_note(self, user_id: int, name: str, tags: list[str] | tuple[str, ...]):
        requests.post(f'{self._server}/user/{user_id}/add_note', json={"name": name, "tags": tags})

    def get_notes(self):
        return requests.get(f'{self._server}/{self._addresses.users}').content

    def get_users(self, since: datetime):
        return requests.get(f'{self._server}/{self._addresses.users}?since={since}').content

    def get_user_data(self, user_id: int):
        return requests.get(f'{self._server}/user/data')


if __name__ == '__main__':
    requester = Requester('http://127.0.0.1:5000')
