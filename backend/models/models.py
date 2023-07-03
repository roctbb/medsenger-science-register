import enum

from .alchemy import db, backref
from .relation_tables import *
from backend.helpers import *


class Sex(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    sex = db.Column(db.Enum(Sex), nullable=True)
    birthday = db.Column(db.Date, nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    records = db.relationship('Record', backref=backref('patient', uselist=False), lazy=True)
    submissions = db.relationship('FormGroupSubmission', backref=backref('patient', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "birthday": self.birthday.isoformat()
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    patients = db.relationship('Patient', secondary=project_patient, backref='projects')
    form_groups = db.relationship('FormGroup', backref=backref('project', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    projects = db.relationship('Project', secondary=project_clinic, backref='clinics', lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "projects": as_dict(self.projects)
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    clinics = db.relationship('Clinic', secondary=user_clinic, backref='doctors', lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "clinics": as_dict(self.clinics)
        }


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


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    fields = db.Column(db.JSON, nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "fields": self.fields
        }


class FormGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)
    forms = db.relationship('Form', secondary=form_group, backref='groups', lazy=False)
    submissions = db.relationship('FormGroupSubmission', backref=backref('group', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "forms": as_dict(self.forms)
        }


class FormGroupSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('form_group.id', ondelete="CASCADE"), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"))

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    records = db.relationship('Record', backref=backref('submission', uselist=False, lazy=True), lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "group": self.group.as_dict(),
            "description": self.description,
            "records": as_dict(self.records)
        }
