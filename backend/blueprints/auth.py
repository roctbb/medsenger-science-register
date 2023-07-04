from flask import Blueprint, request
from backend.methods import *

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth', methods=['post'])
@creates_response
def check_credentials():
    data = request.json

    user, token = authorize_by_credentials(data.get('email'), data.get('password'))

    return {
        "user": user.as_dict(),
        "api_token": token.as_dict()
    }
