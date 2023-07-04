from .alchemy import *

user_clinic = db.Table('user_clinic',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE")),
                       db.Column('clinic_id', db.Integer, db.ForeignKey('clinic.id', ondelete="CASCADE"))
                       )

project_clinic = db.Table('project_clinic',
                          db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE")),
                          db.Column('clinic_id', db.Integer, db.ForeignKey('clinic.id', ondelete="CASCADE"))
                          )

project_patient = db.Table('project_patient',
                           db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE")),
                           db.Column('patient_id', db.Integer, db.ForeignKey('patient.id', ondelete="CASCADE"))
                           )

form_in_groups = db.Table('form_in_groups',
                      db.Column('form_id', db.Integer, db.ForeignKey('form.id', ondelete="CASCADE")),
                      db.Column('group_id', db.Integer, db.ForeignKey('form_group.id', ondelete="CASCADE"))
                      )
