from .alchemy import *
from .relation_tables import *
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import JSON


class FormPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    fields = db.Column(JSON, nullable=True)
    repeatable = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "fields": self.fields,
            "repeatable": self.repeatable,
        }


class FormCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    priority = db.Column(db.Integer, default=0)

    forms = db.relationship('Form', backref=backref('category', uselist=False, lazy=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
        }


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('form_category.id', ondelete="set null"), nullable=True)

    parts = db.relationship('FormPart', secondary=form_form_part, order_by=form_form_part.c.index, backref='forms',
                            lazy=False)
    submissions = db.relationship('FormSubmission', backref=backref('form', uselist=False), lazy=True)

    specialty = db.Column(db.String(256), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parts": as_dict(self.parts),
            "specialty": self.specialty,
            "category_id": self.category_id
        }


class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id', ondelete="CASCADE"), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    is_legacy = db.Column(db.Boolean, default=False)

    records = db.relationship('Record', backref=backref('submission', uselist=False, lazy=True), lazy=False)
    comments = db.relationship('Comment', backref=backref('submission', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "form_id": self.form_id,
            "patient_id": self.patient_id,
            "project_id": self.project_id,
            "records": as_dict(self.records),
            "created_on": self.created_on.isoformat() + 'Z',
            "author": self.doctor.name if self.doctor else None
        }
