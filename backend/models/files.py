from .alchemy import *
from .relation_tables import *
from sqlalchemy.dialects.postgresql import UUID
import uuid


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    type = db.Column(db.String(256), nullable=True)

    path = db.Column(db.String(256), nullable=True)
    file_name = db.Column(db.String(256), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "path": self.path,
            "file_name": self.file_name,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "project_id": self.project_id,
            "created_on": self.created_on.isoformat()
        }