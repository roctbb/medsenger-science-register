from secrets import token_hex

from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def place_comment(project, patient, doctor, text, description=None):
    if not text:
        raise InsufficientData

    comment = Comment(patient_id=patient.id, project_id=project.id, doctor_id=doctor.id, text=text,
                      description=description)
    db.session.add(comment)

    return comment
