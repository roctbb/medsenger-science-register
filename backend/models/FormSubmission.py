from .relation_tables import *


class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id', ondelete="CASCADE"), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    is_legacy = db.Column(db.Boolean, default=False)

    records = db.relationship('Record', backref=backref('submission', uselist=False, lazy=True), lazy=False)
    comments = db.relationship('Comment', backref=backref('submission', uselist=False), lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "form_id": self.form_id,
            "patient_id": self.patient_id,
            "project_id": self.project_id,
            "records": as_dict(self.records),
            "created_on": self.created_on.isoformat() + 'Z',
            "author": self.doctor.name if self.doctor else None
        }
