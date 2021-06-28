from sqlalchemy.sql import func
from project import db
from sqlalchemy_serializer import SerializerMixin

class Team(db.Model, SerializerMixin):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    stam_id = db.Column(db.Integer)
    suffix = db.Column(db.String(128), nullable=True)
    colors = db.Column(db.String(128), nullable=False)

    def __init__(self, id, stam_id, suffix, colors):
        self.id = id
        self.stam_id = stam_id
        self.suffix = suffix
        self.colors = colors

    def as_json(self):
        return {"id": self.id, "stam_id": self.stam_id, "colors": self.colors, "suffix": self.suffix}
