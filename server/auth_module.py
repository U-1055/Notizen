from datetime import datetime, timezone, timedelta
from pathlib import Path
import bcrypt
import hashlib
import jwt
import shelve
import logging as log

logger = log.getLogger()
logger.setLevel(log.WARNING)


class Authenticator:

    def __init__(self, access_token_lifetime: timedelta, refresh_token_lifetime: timedelta, jwt_alg: str):
        """

        :param access_token_lifetime: время жизни access-токена (в минутах).
        :param refresh_token_lifetime: время жизни refresh-токена (в часах).
        """
        self._tokens = {}  # {'<session_token>': {'login': login, 'user_id': user_id}}
        self._access_token_lifetime = access_token_lifetime
        self._refresh_token_lifetime = refresh_token_lifetime
        self._jwt_alg = jwt_alg

    def _create_refresh_token(self, login: str) -> str:
        time_utc = datetime.now(timezone.utc)
        key = self._get_secret()
        refresh_token_invalid_time = time_utc + self._refresh_token_lifetime
        refresh_token = jwt.encode(
            payload={
                'login': login,
                'exp': refresh_token_invalid_time
            },
            key=key,
            algorithm=self._jwt_alg
        )
        logger.warning(f'refresh-token created: exp_time: {refresh_token_invalid_time}')
        return refresh_token

    def delete_token(self, login: str):
        self._tokens.pop(login)

    def _get_secret(self) -> str:
        """Возвращает ключ подписи JWT."""
        with shelve.open('storage', 'r') as storage:
            return storage['secret']

    def get_user_login(self, token_: str) -> str | None:
        try:
            user_info = jwt.decode(token_, algorithms=self._jwt_alg)
            logger.warning(f'get_user_login: token: {user_info}')
            return user_info['login']
        except jwt.ExpiredSignatureError as e:
            return

    def check_token_login(self, login: str, token: str) -> bool:
        """Проверка токена через логин пользователя."""
        return self._tokens[token]['login'] == login

    def check_token_id(self, user_id: int, token: str) -> bool:
        """Проверка токена через user_id пользователя."""
        return self._tokens[token]['user_id'] == user_id

    def check_token(self, token: str) -> bool:
        try:
            token_info = jwt.decode(token, algorithms=self._jwt_alg)
            if token_info:
                return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def update_tokens(self, refresh_token: str) -> dict | None:
        """Обновляет пару токенов по refresh-токену. Возвращает access- и refresh-токены."""

        try:
            token_ = jwt.decode(refresh_token, self._get_secret(), algorithms=self._jwt_alg)
            new_tokens = self.get_tokens(token_['login'])
            return new_tokens
        except jwt.ExpiredSignatureError:
            return
        except jwt.InvalidTokenError:
            return
        except KeyError:
            return

    def get_tokens(self, login: str) -> dict:
        """Отдаёт пару токенов access+refresh."""
        for token_ in self._tokens:
            if self._tokens[token_]['login'] == login:
                return token_

        access_token_invalid_time = datetime.now(timezone.utc) + self._access_token_lifetime
        refresh_token_invalid_time = datetime.now(timezone.utc) + self._refresh_token_lifetime
        key = self._get_secret()

        access_token = jwt.encode(
            payload={
                'login': login,
                'exp': access_token_invalid_time,
            },
            key=key,
            algorithm=self._jwt_alg
        )

        refresh_token = self._create_refresh_token(login)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
                }

def get_hash(string: str) -> str:
    hash_ = bcrypt.hashpw(bytes(string, encoding='utf-8'), bcrypt.gensalt())
    return hash_.decode('utf-8')

