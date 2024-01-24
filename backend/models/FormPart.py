from .alchemy import *
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