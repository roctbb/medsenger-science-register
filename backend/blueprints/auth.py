from flask import Blueprint, request
from backend.methods import *

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth', methods=['post'])
@creates_response
def check_credentials():
    data = request.json

    user, token = authorize_by_credentials(data.get('email'), data.get('password'))

    user_description = user.as_dict()
    user_description.update(token.as_dict())

    return user_description


@auth_blueprint.route('/user', methods=['get'])
@creates_response
@requires_user
def get_user(user):
    return user.as_dict()