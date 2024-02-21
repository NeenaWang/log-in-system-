from inspect import signature
from random import getrandbits
from bottle import redirect, request
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Session(Base):
    __tablename__ = "sessions"

    username = Column(String, primary_key=True)
    id = Column(Integer)

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username


def create_session(db, username):
    session = Session(username=username, id=getrandbits(32))
    db.add(session)
    return session


def get_session(db, id):
    return db.query(Session).filter_by(id=id).first()


def get_session_by_username(db, username):
    return db.query(Session).get(username)


def delete_session(db, session):
    db.delete(session)


def logged_in(f):
    def wrapper(db, *args, **kwargs):
        sess_id = request.get_cookie("session")
        session = get_session(db, int(sess_id)) if (sess_id is not None) else None
        if session is None:
            return redirect("/login")
        kwargs["session"] = session
        if "db" in signature(f).parameters:
            kwargs["db"] = db
        return f(*args, **kwargs)
    return wrapper

