'''Structure of the table in database'''

from sqlalchemy.orm import Mapped, mapped_column 
from flask_login import  UserMixin

from resources import db

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    password_hash: Mapped[str]

