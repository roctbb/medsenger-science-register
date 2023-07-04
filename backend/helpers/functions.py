import hashlib
from flask import jsonify


class ExplainableException(Exception):
    def explain(self):
        return self.__class__.__name__

    def status(self):
        return 422


def hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def make_error(reason='', code=422):
    if isinstance(reason, ExplainableException):
        reason = reason.explain()

    return jsonify({
        "state": "error",
        "error": reason
    }), code


def make_result(data, code=200):
    return jsonify({
        "state": "success",
        "data": data
    }), code
