from flask import Flask, request, abort, Response, jsonify
import requests
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import logging
import bcrypt

from multiprocessing import Process
from datetime import datetime
import typing as tp

import server.models as db
from server.model import DataModel
from src.base import DataStructConst
from server.auth_module import Authenticator, get_hash
from server.models import init_db
from server.base import APIResponses

app = Flask('Notizen')
engine = create_engine('sqlite:///database.db')
init_db(engine)
DBSession = sessionmaker(engine)
data_model = DataModel(engine, DBSession)
authenticator = Authenticator()
responses = APIResponses()
logger = logging.getLogger()


def response(status_code: int, data: tp.Any) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp.set_data(data)

    return resp


@app.route('/users', methods=['GET'])
def get_users():
    since = request.args.get('since')
    return since


@app.route('/user/<int:user_id>/add_note', methods=['POST'])
def add_note(user_id: int):
    args = request.json
    data_model.add_note(user_id, args['name'], args['tags'])


@app.route('/user/<string:login>/data', methods=['GET'])
def get_user_data(login: str) -> Response:
    return jsonify(data_model.get_user_data(login))


@app.route('/user/<string:session_token>/check_auth', methods=['POST'])
def authorize_by_token(session_token: str) -> str | ValueError:  # Возвращает логин по токену
    login = authenticator.get_user_login(session_token)
    if login:
        return login
    abort(401, responses.unauth)


@app.route('/authorize/<string:login>/<string:password>', methods=['GET'])
def authorize(login: str, password: str) -> str | ValueError:
    users = data_model.get_users()
    if login in users:
        user_password = data_model.get_password_hash(login)

        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user_password, 'utf-8')):  # Сохранённый пароль - хэш пароля
            user_id = data_model.get_user_id(login)
            session_token = authenticator.get_token(login, user_id)
            return session_token
    abort(400, 'Unknown login or password')


@app.route('/register/<string:login>/<string:password>', methods=['POST'])
def register(login: str, password: str):
    users = data_model.get_users()
    if login in users:  # Пользователь существует
        abort(response(400, responses.unknown_arg))
    else:
        print('try to add user')
        data_model.add_user(login, get_hash(password))
        print('user_added')


@app.route('/<int:user_id>/notes', methods=['GET'])
def get_notes(user_id: int):
    token_ = request.authorization.token
    if authenticator.check_token_id(user_id, token_):  # Проверка токена
        return data_model.get_notes(user_id)
    else:
        abort(response(401, 'Unauthorized'))


def run():
    app.run()


def run_server():
    server_process = Process(target=run)
    server_process.start()


local_host = 'http://127.0.0.1:5000'
if __name__ == '__main__':
    run_server()
