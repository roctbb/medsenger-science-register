from .alchemy import *
from .relation_tables import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=True)

    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id', ondelete="set null"), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    auth_tokens = db.relationship('UserToken', backref=backref('user', uselist=False, lazy=False), lazy=True)
    specialties = db.Column(db.JSON, nullable=True)
    activation_key = db.Column(db.String(256), nullable=True)
    password_reset_key = db.Column(db.String(256), nullable=True)

    submissions = db.relationship('FormSubmission', backref=backref('doctor', uselist=False), lazy=True)
    patients = db.relationship('Patient', backref=backref('doctor', uselist=False), lazy=True)
    comments = db.relationship('Comment', backref=backref('doctor', uselist=False), lazy=True)

    def as_dict(self):
        info = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "specialties": self.specialties
        }

        if self.clinic:
            info["clinic"] = self.clinic.as_dict()
            info["projects"] = as_dict(self.clinic.projects)

        return info