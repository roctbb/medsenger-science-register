import enum

from .alchemy import *
from .relation_tables import *


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
    doctors = db.relationship('User', backref=backref('clinic', uselist=False), lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "projects": as_dict(self.projects)
        }
