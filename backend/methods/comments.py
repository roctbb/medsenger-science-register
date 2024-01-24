from secrets import token_hex

from backend.models import *
from .exceptions import *
from .patients import mark_updated
from backend.helpers import *


@transaction
def place_comment(project, patient, doctor, text, description=None, submission_id=None):
    if not text:
        raise InsufficientData

    comment = Comment(patient_id=patient.id, project_id=project.id, doctor_id=doctor.id, text=text,
                      description=description, submission_id=submission_id)
    db.session.add(comment)

    mark_updated(patient)

    return comment
