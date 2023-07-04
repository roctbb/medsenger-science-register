from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


def as_dict(iterable):
    return [element.as_dict() for element in iterable]
