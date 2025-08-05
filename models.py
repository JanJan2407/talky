'''Structure of the table in database'''

from sqlalchemy.orm import Mapped, mapped_column
from flask_login import  UserMixin

from resources import db

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(unique = True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    password_hash: Mapped[str]

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str]
    title: Mapped[str]
    post_content: Mapped[str]
    time: Mapped[int] # Time since epoch 1st of January 1970 in UTC timezone, gets converted to actual time with users timezone
    likes: Mapped[str] = mapped_column(default = '{"count" : 0, "names" : []}' ) # In JSON holding a disctionary with amount of likes and a list of all usernames that liked same structure used for dislikes
    dislikes: Mapped[str] = mapped_column(default = '{"count" : 0, "names" : []}' )
    comments: Mapped[str] = mapped_column(default = '[]')
    comment_id: Mapped[int] = mapped_column(default = 0) # Keeps track of how many comments in total were placed on a perticular post
