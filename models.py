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
    image_count: Mapped[int] = mapped_column(default = 0) # Images stored in a separate folder
    post_content: Mapped[str]
    time: Mapped[int] # Time since epoch 1st of January 1970 in UTC timezone, gets converted to actual time with users timezone

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int]
    username: Mapped[str]
    content: Mapped[str]
    time: Mapped[int]  # epoch time
    likes: Mapped[str] = mapped_column(default = '{"count" : 0, "names" : []}' ) # In JSON holding a dictionary with amount of likes and a list of all usernames that liked same structure used for dislikes
    dislikes: Mapped[str] = mapped_column(default = '{"count" : 0, "names" : []}' )
    parent_id: Mapped[int] = mapped_column(nullable = True, default = None) # parent_id is used to link comments to their parent comment, if it's None then it's a top-level comment, used for comment replies

class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    post_id: Mapped[int]
    comment_id: Mapped[int] = mapped_column(nullable = True, default = None)  # None for post, set for comment
    username: Mapped[str]
    is_like: Mapped[bool]  # True for like, False for dislike