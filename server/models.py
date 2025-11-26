import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_base, mapped_column, relationship, sessionmaker, Session
from sqlalchemy import String, ForeignKey, ClauseList, create_engine, Engine, MetaData, Date

from typing import Optional
from contextlib import contextmanager


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    tags = relationship('Tag')
    notes = relationship('Note')

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }


class Tag(Base):
    __tablename__ = 'tag'

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class NoteTag(Base):
    __tablename__ = 'note_tag'
    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tag.id'))
    note_id: Mapped[int] = mapped_column(ForeignKey('note.id'))


class NoteFile(Base):
    __tablename__ = 'note_file'
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String())


class Note(Base):
    __tablename__ = 'note'

    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    file_id: Mapped[int] = mapped_column(ForeignKey('note_file.id'))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date_changing: Mapped[datetime.datetime] = mapped_column(default=datetime.date.today())
    tags = relationship(Tag, secondary='note_tag')
    user = relationship(User, back_populates='notes')
    file = relationship(NoteFile)

    def serialize(self) -> dict:
        return {
            'user_id': self.user_id,
            'file_id': self.file_id,
            'id': self.id,
            'name': self.name,
            'date_changing': self.date_changing,
        }


def get_engine() -> Engine:
    return create_engine('sqlite:///db/database.db')


def init_db(engine: Engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db(create_engine('sqlite:///database.db', echo=True))
