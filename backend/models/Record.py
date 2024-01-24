
from backend.helpers import *
from .RecordType import *
from sqlalchemy.dialects.postgresql import JSON

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    category_id = db.Column(db.Integer, db.ForeignKey('record_category.id', ondelete="SET null"), nullable=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('form_submission.id', ondelete="SET null"), nullable=True)

    value = db.Column(db.Text, nullable=True)
    params = db.Column(JSON, nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "params": self.params,
            "category": self.category.as_dict(),
            "created_on": self.created_on.isoformat() + 'Z',
            "value": self.formatted_value()
        }

    def formatted_value(self):
        try:
            if self.category.type == RecordType.INTEGER:
                return int(self.value)
            if self.category.type == RecordType.FLOAT:
                return float(self.value.replace(',', '.'))
        except:
            pass

        return self.value
