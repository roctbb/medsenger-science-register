from .alchemy import *

class FormCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    priority = db.Column(db.Integer, default=0)
    forms = db.relationship('Form', backref=backref('category', uselist=False, lazy=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority
        }