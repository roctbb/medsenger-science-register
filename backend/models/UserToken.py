from .alchemy import *
from .relation_tables import *


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    token = db.Column(db.String(256), nullable=False)


    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    expire_on = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        return {
            "api_token": self.token,
            "expire_on": self.expire_on.isoformat() + "Z",
        }
