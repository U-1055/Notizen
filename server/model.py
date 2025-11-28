import datetime
import logging as log

from src.interfaces import IModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Engine, select, insert, delete, update

import server.models as db
from server.models import User
import typing as tp
from contextlib import contextmanager


logger = log.getLogger()


class DataModel:

    def __init__(self, db_engine: Engine, session_fabric: tp.Callable):
        self._db_engine = db_engine
        self._session_maker = session_fabric

    def _check_limit_offset(self, limit: int, offset: int, length: int) -> list[int | None, ...]:
        result = [None, None]
        if 0 <= limit < length:
            result[0] = limit
        if 0 <= offset < length:
            result[1] = offset
        return result

    def get_users(self, limit: int = None, offset: int = None) -> tuple[str, ...]:
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

    def get_user_login(self, user_id: int) -> str:
        with self._session_maker() as session, session.begin():
            login = session.scalar(select(db.User.name).where(db.User.id == user_id))
        return login

    def get_user_data(self, login: str) -> dict | None:
        with self._session_maker() as session, session.begin():
            session: Session
            user_data = session.execute(select(db.User).where(db.User.name == login)).one()
            if user_data[0]:
                return user_data[0].serialize()

    def get_notes(self, user_id: int, names: tuple = None, tags: tuple = None, limit: int = 0, offset: int = 0):

        query = select(db.Note).join(db.User).where(db.User.id == user_id)
        if names:
            query = query.where(db.Note.name == names)
        if tags:
            query = query.join(db.NoteTag, onclause=db.Note.id == db.NoteTag.note_id).join(db.Tag, onclause=db.Tag.id == db.NoteTag.tag_id).where(db.Tag.name.in_(tags))

        with self._session_maker() as session, session.begin():
            session: Session
            notes = session.execute(query)
            notes = [note[0] for note in notes]

            return [note.serialize() for note in notes[offset:]]

    def update_note(self, user_id: int, name: str, tags: list, content: str, date_changing: str):
        date_changing = datetime.datetime.strptime(date_changing, '%d.%m.%Y')

        with self._session_maker() as session, session.begin():
            session.execute(update(db.Note).where(db.Note.user_id == user_id and db.Note.name == name), {'date_changing': date_changing})

    def delete_note(self, user_id: int, name: str):
        with self._session_maker() as session, session.begin():
            session.execute(delete(db.Note).where(db.Note.user_id == user_id).where(db.Note.name == name))

    def add_tag(self, user_id: int, name: str):
        with self._session_maker() as session, session.begin():
            session.add(db.Tag(user_id=user_id, name=name))

    def get_tags(self, user_id: int, names: tuple[str, ...] = None, notes: tuple[str, ...] = None, limit: int = None, offset: int = None) -> tuple[db.Tag, ...]:
        query = select(db.Tag).where(db.Tag.user_id == user_id)
        if names:
            query = query.where(db.Tag.name.in_(names))

        if limit is None:
            limit = 0
        if offset is None:
            offset = 0

        with self._session_maker() as session, session.begin():
            session.execute(query)

    def get_users_ids(self) -> tuple[str, ...]:
        with self._session_maker() as session, session.begin():
            session: Session
            users = session.scalars(select(db.User.id))

        return [user for user in users]

    def get_user_tags(self, user_id: str):
        with self._session_maker() as session, session.begin():
            tags = session.scalars(select(db.Tag).where(db.Tag.user_id == user_id))
        return tags

    def get_note_names(self, user_id: int) -> tuple[str, ...]:
        with self._session_maker() as session, session.begin():
            user_notes = session.query(db.Note.name).where(db.Note.user_id == user_id)
        return tuple(user_notes)

    def add_note(self, user_id: int, name: str, tags: list[str] | tuple[str, ...]):

        if name in self.get_note_names(user_id):
            raise ValueError('Name of the note must be unique.')

        with self._session_maker() as session, session.begin():
            tag_ids = session.query(db.Tag).join(db.User).where(db.User.id == user_id and db.Tag.name in tags)
            note = db.Note(user_id=user_id, name=name, file_id=1)
            session.add(note)
            logger.warning(f'Add note: {name}, tags: {tags}')

        with self._session_maker() as session, session.begin():
            for id_ in tag_ids:
                session.add(db.NoteTag(note_id=note.id, tag_id=id_, file_id=1))

    def add_user(self, name: str, hashed_password: str):
        with self._session_maker() as session, session.begin():
            user = db.User(name=name, password=hashed_password)
            session.add(user)

def db_config_1(session: Session):
    for i in range(50):
        user = db.User(name=f'user#{i}')
        session.add(user)
        session.commit()
        for i1 in range(10):
            tag = db.Tag(name=f'tag#{i1}', user_id=user.id)
            session.add(tag)


if __name__ == '__main__':
    from server.models import init_db
    engine = create_engine('sqlite:///database.db', echo=True)
    with Session(bind=engine) as session, session.begin():
        result = session.execute(select(db.Note).where(db.Note.user_id == 2))
        print([note for note in result])

