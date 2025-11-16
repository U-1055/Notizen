from pathlib import Path
import bcrypt
import hashlib


class Authenticator:

    def __init__(self):
        self._tokens = {}  # {'<session_token>': {'login': login, 'user_id': user_id}}

    def delete_token(self, login: str):
        self._tokens.pop(login)

    def get_user_login(self, token_: str) -> str:
        user_info = self._tokens.get(token_)
        if user_info:
            return user_info['login']

    def check_token_login(self, login: str, token: str) -> bool:
        """Проверка токена через логин пользователя."""
        return self._tokens[token]['login'] == login

    def check_token_id(self, user_id: int, token: str) -> bool:
        """Проверка токена через user_id пользователя."""
        return self._tokens[token]['user_id'] == user_id

    def get_token(self, login: str, user_id: int) -> str:
        """Отдаёт токен сессии."""
        for token_ in self._tokens:
            if self._tokens[token_]['login'] == login:
                return token_

        token_ = get_hash(login)
        self._tokens[token_] = {'login': login, 'user_id': user_id}
        return token_


def get_hash(string: str) -> str:
    hash_ = bcrypt.hashpw(bytes(string, encoding='utf-8'), bcrypt.gensalt())
    return hash_.decode('utf-8')

