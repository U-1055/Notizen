import json

import requests

import datetime

from server.base import ServerInfo
from src.base import APIResponses


def form_request(server: str, *args) -> str:
    return f'{server}{''.join([f'/{el}' for el in args])}'


class HttpError400(Exception):
    pass


class HttpError401(Exception):
    pass


class Requester:

    def __init__(self, server: str, addresses: ServerInfo = ServerInfo()):
        self._server = server
        self._addresses = addresses

    def _send_request(self, request: requests.Response):
        """Обрабатывает ответ запроса и вызывает нужные исключения."""
        if request.status_code == 401:
            raise HttpError401(request)
        elif request.status_code == 400:
            raise HttpError400(request)

    def check_authorize(self, token_: str):
        request = requests.post(url=f'{self._server}/user/{token_}/check_auth')
        if request.status_code == 401:
            raise HttpError401(APIResponses.unauth)
        return request.request

    def authorize(self, login: str, password: str):
        request = requests.get(f'{self._server}/authorize/{login}/{password}')
        if request.status_code == 400:
            raise HttpError400(APIResponses.unknown_arg)

    def add_note(self, user_id: int, name: str, tags: list[str] | tuple[str, ...]):
        requests.post(f'{self._server}/user/{user_id}/add_note', json={"name": name, "tags": tags})

    def get_user_notes(self, user_id: int, token_: str) -> tuple:
        """Возвращает список заметок (их моделей)."""
        request = requests.get(f'{self._server}/{user_id}/notes', auth=token_)
        if request.status_code == 401:
            raise HttpError401(APIResponses().unauth)

        return request.content

    def get_user_tags(self, user_id: int, token_: str) -> tuple:
        """Возвращает список тегов пользователя."""
        pass

    def get_note(self, user_id: int, note: str):
        pass

    def get_users(self, since: datetime):
        return requests.get(f'{self._server}/{self._addresses.users}?since={since}').content

    def get_user_data(self, login: str) -> dict:
        return requests.get(f'{self._server}/user/{login}/data').json()

    def get_note_tags(self, user_id: int, note: str, token_: str):
        pass

    def register(self, login: str, password: str):
        request = requests.post(f'{self._server}/register/{login}/{password}')

        if request.status_code == 400:
            raise HttpError400(APIResponses.unknown_arg)


if __name__ == '__main__':
    requester = Requester('http://127.0.0.1:5000')
