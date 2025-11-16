import datetime

from src.interfaces import IModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Engine, select, insert

import server.models as db
from server.models import User
import typing as tp
from contextlib import contextmanager


class DataModel:

    def __init__(self, db_engine: Engine, session_fabric: tp.Callable):
        self._db_engine = db_engine
        self._session_maker = session_fabric

    def get_users(self) -> tuple[str, ...]:
        with self._session_maker() as session, session.begin():
            users = session.scalars(select(db.User.name))
        return users

    def get_password_hash(self, login: str) -> str:
        with self._session_maker() as session, session.begin():
            password = session.scalar(select(db.User.password).where(db.User.name == login))
        return password

    def get_user_id(self, name: str) -> int:
        with self._session_maker() as session, session.begin():
            id_ = session.scalar(select(db.User.id).where(db.User.name == name))
        return id_

    def get_user_data(self, login: str) -> dict:
        with self._session_maker() as session, session.begin():
            session: Session
            user_data = session.execute(select(db.User).where(db.User.name == login)).first()
            return user_data[0].serialize()

    def get_users_ids(self) -> tuple[str, ...]:
        with self._session_maker() as session, session.begin():
            session: Session
            users = session.scalars(select(db.User.id))

        return [user for user in users]

    def get_user_tags(self, user_id: str):
        with self._session_maker() as session, session.begin():
            tags = session.scalars(select(db.Tag).where(db.Tag.user_id == user_id))
        return tags

    def get_notes(self, user_id: int) -> tuple[str, ...]:
        with self._session_maker() as session, session.begin():
            user_notes = session.query(db.Note.name).where(db.Note.user_id == user_id)
        return tuple(user_notes)

    def add_tag(self, user_id: int, name: str):
        with self._session_maker() as session, session.begin():
            tag = db.Tag(user_id=user_id, name=name)
            session.add(tag)

    def add_note(self, user_id: int, name: str, tags: list[str] | tuple[str, ...]):

        with self._session_maker() as session, session.begin():
            tag_ids = session.query(db.Tag).join(db.User).where(db.User.id == user_id and db.Tag.name in tags)
            session.add(db.Note(user_id=user_id, name=name, tags=[id_ for id_ in tag_ids]))

    def add_user(self, name: str, hashed_password: str):
        with self._session_maker() as session, session.begin():
            session.add(db.User(name=name, password=hashed_password))


def db_config_1(session: Session):
    for i in range(50):
        user = db.User(name=f'user#{i}')
        session.add(user)
        session.commit()
        for i1 in range(10):
            tag = db.Tag(name=f'tag#{i1}', user_id=user.id)
            session.add(tag)


if __name__ == '__main__':
    from server.models import init_db, User
    engine = create_engine('sqlite:///database.db', echo=True)
    init_db(engine)
    session_fabric = sessionmaker(engine)

    data_model = DataModel(engine, session_fabric)
    data_model.add_user('user1', '12345')
