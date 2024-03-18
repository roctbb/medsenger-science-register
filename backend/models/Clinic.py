from .relation_tables import *


class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = db.relationship('Project', secondary=project_clinic, backref='clinics', lazy=False)
    doctors = db.relationship('User', backref=backref('clinic', uselist=False), lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
