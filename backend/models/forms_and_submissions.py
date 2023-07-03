from .alchemy import db, backref
from .relation_tables import *
from backend.helpers import *


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
    forms = db.relationship('Form', secondary=form_in_groups, backref='groups', lazy=False)
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
