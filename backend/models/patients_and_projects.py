import enum

from .alchemy import *
from .relation_tables import *


class Sex(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    sex = db.Column(db.Enum(Sex), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    records = db.relationship('Record', backref=backref('patient', uselist=False), lazy=True)
    submissions = db.relationship('FormSubmission', backref=backref('patient', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "email": self.email,
            "birthday": self.birthday.isoformat()
        }


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id
        }



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    patients = db.relationship('Patient', secondary=project_patient, backref='projects')
    forms = db.relationship('Form', backref=backref('project', uselist=False), lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "forms": as_dict(self.forms)
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
