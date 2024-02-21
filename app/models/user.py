from sqlalchemy import Column, Integer, String
import os, hashlib
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String)
    coins = Column(Integer)
    salt = Column(String)

    def get_coins(self):
        return self.coins

    def credit_coins(self, i):
        self.coins += i

    def debit_coins(self, i):
        self.coins -= i

def create_user(db, username, password):
    salt = os.urandom(16).hex()
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

    user = User(
        username=username,
        password=hashed_password,
        salt=salt,
        coins=100,
    )
    db.add(user)
    db.commit()
    return user

def get_user(db, username):
    return db.query(User).filter_by(username=username).first()
