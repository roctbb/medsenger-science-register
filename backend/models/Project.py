from .relation_tables import *
from ..helpers import collect_categories


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patients = db.relationship('Patient', secondary=project_patient, backref='projects')
    forms = db.relationship('Form', backref=backref('project', uselist=False), lazy=False)

    steps = db.Column(db.JSON, nullable=True)

    show_files = db.Column(db.Boolean, default=False)
    show_comments = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "forms": as_dict(self.forms),
            "steps": self.steps,
            "categories": as_dict(collect_categories(self.forms)),
            "settings": {
                "show_files": self.show_files,
                "show_comments": self.show_comments
            }
        }
