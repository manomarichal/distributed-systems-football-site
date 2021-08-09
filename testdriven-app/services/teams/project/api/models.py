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

class Club(db.Model, SerializerMixin):
    __tablename__ = 'clubs'
    stam_id = db.Column(db.Integer)
    name = db.Column(db.String(128), nullable=False, primary_key = True) # TODO change to stam id primary id
    address = db.Column(db.String(128), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(128), nullable=False)
    website = db.Column(db.String(128), nullable=False)

    def __init__(self, stam_id, name, address, zip_code, city, website):
        self.stam_id = stam_id
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.website = website