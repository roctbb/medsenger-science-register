from .relation_tables import *


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('form_category.id', ondelete="set null"), nullable=True)

    parts = db.relationship('FormPart', secondary=form_form_part, order_by=form_form_part.c.index, backref='forms',
                            lazy=False)
    submissions = db.relationship('FormSubmission', backref=backref('form', uselist=False), lazy=True)

    specialty = db.Column(db.String(256), nullable=True)
    is_legacy = db.Column(db.Boolean, default=False, server_default="false")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parts": as_dict(self.parts),
            "specialty": self.specialty,
            "category_id": self.category_id,
            "is_legacy": self.is_legacy
        }
