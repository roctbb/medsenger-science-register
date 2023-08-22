import time

from backend.models import db
from flask import request
from .functions import *
import traceback
import sys


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
        S = time.time()
        result = None
        try:
            result = make_result(func(*args, **kwargs))
        except ExplainableException as e:
            result = make_error(e, e.status())
        except Exception as e:
            print(traceback.format_exc())
            print("ServerError", e)
            result = make_error('ServerError', 500)

        E = time.time()

        print(f"Request took {E - S} secs")

        return result

    wrapper.__name__ = func.__name__
    return wrapper
