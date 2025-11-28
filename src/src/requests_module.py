import json
import time

import requests
import typing as tp
import datetime

from server.base import ServerInfo
from server.api_answers import APIResponseStruct
from src.base import APIResponses


def form_request(server: str, *args) -> str:
    return f'{server}{''.join([f'/{el}' for el in args])}'


def form_headers(auth: str) -> dict:
    return {
        'Authorization': auth
    }


class HTTPError(Exception):
    pass


class HttpError400(HTTPError):
    pass


class HttpError401(HTTPError):
    pass


class HTTPError500(HTTPError):
    pass


class HTTPError404(HTTPError):
    pass


class Requester:
    """
    API-слой.
    :param request_preparer: вызываемый объект, обрабатывающий ошибки.
    Должен иметь сигнатуру вида func (request: tp.Callable, *args, **kwargs) -> response, где request - обрабатываемый запрос;
    response - ответ, полученный от запроса.
    :param server: адрес сервера.
    """

    def __init__(
            self,
            server: str,
            request_preparer: tp.Callable[[tp.Callable, tp.Any], tp.Any] = None,
            addresses: ServerInfo = ServerInfo(),
            api_responses: APIResponseStruct = APIResponseStruct()
    ):

        self._server = server
        self._addresses = addresses
        self._request_preparer = request_preparer
        self._api_responses = api_responses

    def _prepare_result(self, response: requests.Response):
        """Обрабатывает ответ запроса и вызывает нужные исключения."""
        if response.status_code == 401:
            raise HttpError401(response)
        elif response.status_code == 400:
            raise HttpError400(response)
        elif response.status_code == 404:
            raise HTTPError404

    @staticmethod
    def _preparing_request(func: tp.Callable):
        def prepare_request(self: 'Requester', *args, **kwargs):

            try:
                if self._request_preparer:
                    response = self._request_preparer(func, *(self, *args), **kwargs)
                    return response
                else:
                    return func(self, *args, **kwargs)
            except HTTPError as e:
                raise e

        return prepare_request

    def update_note(self, note_name: str, note_data: dict, user_id: int, token_: str):
        response = requests.put(f'{self._server}/users/{user_id}/notes/{note_name}', json=note_data, headers={'Authorization': token_})
        try:
            self._prepare_result(response)
        except HTTPError as e:
            raise e

    def set_request_preparer(self, preparer: tp.Callable):
        self._request_preparer = preparer

    @_preparing_request
    def update_tokens(self, refresh_token: str) -> dict:
        response = requests.post(f'{self._server}/update_tokens', json={'refresh_token': refresh_token})
        try:
            self._prepare_result(response)
        except HTTPError as e:
            raise e

        return response.json()

    @_preparing_request
    def check_authorize(self, token_: str):
        """

        :param token_: access_token.
        :return:
        """
        request = requests.post(url=f'{self._server}/check_auth', json={'access_token': token_})

        if request.status_code == 401:
            raise HttpError401(APIResponses.unauth)
        return request.json().get(self._api_responses.answer)

    @_preparing_request
    def authorize(self, login: str, password: str) -> dict:
        request = requests.post(f'{self._server}/authorize', json={'login': login, 'password': password})
        if request.status_code == 400:
            raise HttpError400(request.json().get(self._api_responses.error_info))
        response = request.json()
        return {key: response[key] for key in response if key != self._api_responses.status_code}

    @_preparing_request
    def add_note(self, user_id: int, name: str, tags: list[str] | tuple[str, ...], token_: str):
        response = requests.post(f'{self._server}/users/{user_id}/notes', json={"name": name, "tags": tags}, headers=form_headers(token_))
        try:
            self._prepare_result(response)
        except HTTPError as e:
            raise e

    def delete_note(self, user_id: int, name: str, token_: str):
        response = requests.delete(f'{self._server}/users/{user_id}/notes/{name}', headers={'Authorization': token_})
        try:
            self._prepare_result(response)
        except HTTPError as e:
            raise e

    @_preparing_request
    def get_user_notes(self, user_id: int, token_: str) -> tuple:
        """Возвращает список заметок"""
        request = requests.get(f'{self._server}/users/{user_id}/notes', headers=form_headers(token_), params={'limit': 0, 'offset': 0})
        if request.status_code == 401:
            raise HttpError401(APIResponses().unauth)

        return request.json().get(self._api_responses.answer)

    @_preparing_request
    def get_user_tags(self, user_id: int, token_: str) -> tuple:
        """Возвращает список тегов пользователя."""
        pass

    @_preparing_request
    def get_note(self, user_id: int, note: str):
        pass

    @_preparing_request
    def get_users(self, since: datetime):
        return requests.get(f'{self._server}/{self._addresses.users}?since={since}').content

    @_preparing_request
    def get_user_data(self, login: str) -> dict:
        response = requests.get(f'{self._server}/users/{login}')
        return response.json()

    @_preparing_request
    def get_note_tags(self, user_id: int, note: str, token_: str):
        pass

    @_preparing_request
    def register(self, login: str, password: str):
        request = requests.post(f'{self._server}/register', json={'login': login, 'password': password})

        if request.status_code == 400:
            raise HttpError400(APIResponses.unknown_arg)


if __name__ == '__main__':
    requester = Requester('http://127.0.0.1:5000')
