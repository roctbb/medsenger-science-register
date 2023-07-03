from .alchemy import db, backref
from backend.helpers import *
from .relation_tables import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    clinics = db.relationship('Clinic', secondary=user_clinic, backref='doctors', lazy=False)
    auth_tokens = db.relationship('UserToken', backref=backref('user', uselist=False, lazy=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "clinics": as_dict(self.clinics)
        }


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    expire_on = db.Column(db.DateTime, nullable=True)
