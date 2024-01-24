from .relation_tables import *


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
        }
