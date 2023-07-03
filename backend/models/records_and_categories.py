from alchemy import db, backref
from backend.helpers import *
import enum


class RecordType(enum.Enum):
    INTEGER = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    TEXT = 'text'
    DATE = 'date'
    ENUM = 'enum'


class RecordCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    code = db.Column(db.String(256), nullable=True)
    type = db.Column(db.Enum(RecordType))
    params = db.Column(db.JSON, nullable=True)

    records = db.relationship('Record', backref=backref('category', uselist=False, lazy=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type
        }


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('record_category.id', ondelete="SET null"), nullable=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('form_group_submission.id', ondelete="SET null"), nullable=True)

    value = db.Column(db.String(256), nullable=True)
    params = db.Column(db.JSON, nullable=True)
    question_uuid = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "params": self.params,
            "question_uuid": self.question_uuid,
            "category": self.category.as_dict(),
            "created_on": self.created_on.isoformat(),
            "value": self.formatted_value()
        }

    def formatted_value(self):
        if self.category.type == RecordType.INTEGER:
            return int(self.value)
        if self.category.type == RecordType.FLOAT:
            return float(self.value)

        return self.value
