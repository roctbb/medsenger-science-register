from flask import request
from .exceptions import *
from .auth import *


def requires_user(func):
    def wrapper(*args, **kwargs):
        token = request.args.get('api_token')
        user = find_user_by_token(token)
        result = func(user, *args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    return wrapper
