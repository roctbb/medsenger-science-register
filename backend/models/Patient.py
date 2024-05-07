import enum
from .relation_tables import *
from sqlalchemy.dialects.postgresql import JSON


class Sex(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    sex = db.Column(db.Enum(Sex), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(12), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    records = db.relationship('Record', backref=backref('patient', uselist=False), lazy=True)
    submissions = db.relationship('FormSubmission', backref=backref('patient', uselist=False, lazy=True), lazy=True)
    contracts = db.relationship('Contract', backref=backref('patient', uselist=False), lazy=True)
    comments = db.relationship('Comment', backref=backref('patient', uselist=False), lazy=False)
    files = db.relationship('File', backref=backref('patient', uselist=False), lazy=True)
    show_off_records = db.Column(JSON, nullable=True)

    is_legacy = db.Column(db.Boolean, default=False)

    def actual_submissions(self):
        return list(filter(lambda s: not s.is_legacy, self.submissions))

    def as_dict(self, additional_data={}):
        description = {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "email": self.email,
            "phone": self.phone,
            "comments": list(sorted(as_dict(self.comments), key=lambda p: p['created_on'])),
            "created_by": self.doctor.name if self.doctor else "",
            "birthday": self.birthday.isoformat(),
            "updated_on": self.updated_on.isoformat() + "Z" if self.updated_on else None,
            "show_off_records": self.show_off_records if self.show_off_records else []
        }

        description.update(additional_data)

        return description
