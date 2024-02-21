from sqlalchemy import Column, Integer, String

from app.models.base import Base

class PlaintextBreach(Base):
    __tablename__ = "plaintext_breaches"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class HashedBreach(Base):
    __tablename__ = "hashed_breaches"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)

class SaltedBreach(Base):
    __tablename__ = "salted_breaches"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    salted_password = Column(String)
    salt = Column(String)

def create_plaintext_breach_entry(db, username, password):
    breach = PlaintextBreach(
        username=username,
        password=password,
    )
    db.add(breach)
    return breach

def create_hashed_breach_entry(db, username, hashed_password):
    breach = HashedBreach(
        username=username,
        hashed_password=hashed_password,
    )
    db.add(breach)
    return breach

def create_salted_breach_entry(db, username, salted_password, salt):
    breach = SaltedBreach(
        username=username,
        salted_password=salted_password,
        salt=salt,
    )
    db.add(breach)
    return breach

def get_breaches(db, username):
    plaintext_breaches = db.query(PlaintextBreach).filter_by(username=username).all()
    hashed_breaches = db.query(HashedBreach).filter_by(username=username).all()
    salted_breaches = db.query(SaltedBreach).filter_by(username=username).all()
    return (plaintext_breaches, hashed_breaches, salted_breaches)


