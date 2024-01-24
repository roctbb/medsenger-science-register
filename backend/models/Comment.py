from .relation_tables import *

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    submission_id = db.Column(db.Integer, db.ForeignKey('form_submission.id', ondelete="CASCADE"), nullable=True)


    def as_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "description": self.description,
            "created_on": self.created_on.isoformat() + 'Z',
            "author": self.doctor.name if self.doctor else None
        }
