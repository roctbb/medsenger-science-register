from .alchemy import *
from .RecordType import *
from sqlalchemy.dialects.postgresql import JSON


class RecordCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    code = db.Column(db.String(256), nullable=True)
    type = db.Column(db.Enum(RecordType))
    params = db.Column(JSON, nullable=True)

    records = db.relationship('Record', backref=backref('category', uselist=False, lazy=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type
        }