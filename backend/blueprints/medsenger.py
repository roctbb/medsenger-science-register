from flask import Blueprint, request
from backend.methods import *

medsenger_blueprint = Blueprint('medsenger', __name__)


@medsenger_blueprint.route('/medsenger/scenarios', methods=['get'])
@creates_response
@requires_user
def get_medsenger_scenarios(user):
    return medsenger_get_scenarios(user.clinic)