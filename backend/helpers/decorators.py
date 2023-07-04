from backend.models import db
from flask import request
from .functions import *


def transaction(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            raise e

    wrapper.__name__ = func.__name__
    return wrapper


def creates_response(func):
    def wrapper(*args, **kwargs):
        try:
            return make_result(func(*args, **kwargs))
        except ExplainableException as e:
            return make_error(e, e.status())
        except Exception as e:
            print("ServerError", e)
            return make_error('ServerError', 500)

    wrapper.__name__ = func.__name__
    return wrapper
