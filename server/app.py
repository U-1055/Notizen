from flask import Flask, request, abort, Response, jsonify
import requests
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import logging
import bcrypt

from multiprocessing import Process
from datetime import datetime, timedelta
import typing as tp

import server.models as db
from server.model import DataModel
from src.base import DataStructConst
from server.auth_module import Authenticator, get_hash
from server.base import APIResponses
from server.api_answers import APIResponseStruct

app = Flask('Notizen')
engine = create_engine('sqlite:///database.db', echo=True)
DBSession = sessionmaker(engine)
data_model = DataModel(engine, DBSession)
authenticator = Authenticator(access_token_lifetime=timedelta(minutes=15), refresh_token_lifetime=timedelta(hours=24), jwt_alg='HS256')
responses = APIResponses()
api_struct = APIResponseStruct()
logger = logging.getLogger()


def response(status_code: int, data: tp.Any) -> Response:
    resp = Response()
    resp.status_code = status_code

    return resp


def form_error(status_code: int, json_: dict) -> Response:
    """
    Формирует ошибку.
    {
    status_code: xxx,
    json_
    }
    :param status_code: HTTP-код ошибки.
    :param json_: структура ответа.
    :return: Response
    """

    response_ = jsonify(json_)
    response_.status_code = status_code
    return response_


def form_response(status_code: int, json_: dict) -> Response:
    """
    Формирует ответ вида:
    {
    status_code: 200x,
    answer: json_
    }
    :param status_code: HTTP-код ответа.
    :param json_: структура ответа.
    :return Response:
    """

    response_ = jsonify(json_)
    response_.status_code = status_code
    return response_


def check_auth(token: str):
    login = authenticator.get_user_login(token)
    if login:
        return login


@app.route('/users', methods=['GET'])
def users():
    since = request.args.get('since')
    return since


@app.route('/users/<int:user_id>', methods=['GET'])
def user_by_id(user_id: int):
    fields = request.args
    user_data = data_model.get_user_data(data_model.get_user_login(user_id))
    if not authenticator.check_token_id(user_id, request.headers.get('Authorization')):
        return form_error(401, {api_struct.error_info: 'Unauthorized user'})

    if fields:
        user_data = {key: user_data[key] for key in user_data if key in fields}

    return jsonify(user_data)


@app.route('/users/<string:login>', methods=['GET'])
def user_by_login(login: str):
    fields = request.args
    user_data = data_model.get_user_data(login)

    if fields:
        user_data = {key: user_data[key] for key in user_data if key in fields}

    return jsonify(user_data)


@app.route('/users/<int:user_id>/notes', methods=['GET', 'POST', 'PUT'])
def notes(user_id: int):
    token_ = request.headers.get('Authorization')
    if not authenticator.check_token(token_):
        return form_error(401, {api_struct.error_info: 'Unauthorized user'})

    if request.method == 'GET':
        limit = request.args.get(api_struct.limit)
        offset = request.args.get(api_struct.offset)
        if limit:
            limit = int(limit)
        if offset:
            offset = int(offset)

        names = request.args.get('names')
        tags = request.args.get('tags')

        return form_response(200, data_model.get_notes(user_id, names, tags, limit, offset))

    if request.method == 'POST':
        note_params = request.json
        data_model.add_note(user_id, **note_params)

    if request.method == 'PUT':
        note_params = request.json
        data_model.update_note(user_id, **note_params)

    if request.method == 'DELETE':
        name = request.args['name']
        data_model.delete_note(user_id, name)


@app.route('/users/<int:user_id>/tags', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tags():

    if request.method == 'GET':
        limit = request.args.get(api_struct.limit)
        offset = request.args.get(api_struct.offset)
        names = request.args.get('names')
        from_notes = request.args.get('notes')

        return {}

    if request.method == 'POST':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass


@app.route('/check_auth', methods=['POST'])
def authorize_by_token() -> Response:  # Возвращает логин и access_token по refresh-токену
    refresh_token = request.json['refresh_token']
    login = authenticator.get_user_login(refresh_token)
    if login:
        return form_response(200, {api_struct.answer: login})
    return form_error(401, {api_struct.error_info: 'Invalid token'})


@app.route('/authorize', methods=['POST'])
def authorize() -> Response:
    users = data_model.get_users()
    params = request.json
    login, password = params.get('login'), params.get('password')

    if login is None or password is None:
        return form_error(400, {api_struct.error_info: 'No expecting params. The endpoint expected login and password.'})
    if login in users:
        user_password = data_model.get_password_hash(login)
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user_password, 'utf-8')):  # Сохранённый пароль - хэш пароля
            user_id = data_model.get_user_id(login)
            tokens = authenticator.get_tokens(login, user_id)
            return form_response(
                200,
                {
                    api_struct.access_token: tokens['access_token'],
                    api_struct.refresh_token: tokens['refresh_token']
                }
            )
    else:
        return form_error(400, {api_struct.error_info: f'Unregistered user with login: {login}'})


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    login, password = params['login'], params['password']
    users = data_model.get_users()
    if login in users:  # Пользователь существует
        abort(response(400, responses.unknown_arg))
    else:
        data_model.add_user(login, get_hash(password))


def run():
    app.run()


def run_server():
    server_process = Process(target=run)
    server_process.start()


local_host = 'http://127.0.0.1:5000'
if __name__ == '__main__':
    run_server()
