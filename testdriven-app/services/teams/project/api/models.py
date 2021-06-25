from sqlalchemy.sql import func
from project import db

class Team(db.Model):
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

# class Referee(db.Model):
#     first_name = db.Column(db.String(128), nullable=False)
#     last_name = db.Column(db.String(128), nullable=False)
#     last_name = db.Column(db.String(128), nullable=False)