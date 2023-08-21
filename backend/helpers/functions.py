import hashlib
from datetime import datetime

from flask import jsonify
import re


class ExplainableException(Exception):
    def __init__(self, details=None):
        self.details = details
        super().__init__()

    def explain(self):
        return self.__class__.__name__

    def status(self):
        return 422


def hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def gts():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S - ")


def make_error(reason='', code=422):
    if isinstance(reason, ExplainableException):
        details = reason.details
        reason = reason.explain()
    else:
        details = None

    return jsonify({
        "state": "error",
        "error": reason,
        "details": details
    }), code


def make_result(data, code=200):
    return jsonify({
        "state": "success",
        "data": data
    }), code


def check_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat, email):
        return True
    else:
        return False


def collect_categories(forms):
    return sorted(set([category for category in map(lambda form: form.category, forms) if category is not None]), key=lambda c: -c.priority)
