from sqlalchemy.sql import func
from project import db

class Club(db.Model):
    __tablename__ = 'clubs'
    stam_id = db.Column(db.Integer)
    name = db.Column(db.String(128), nullable=False, primary_key = True)
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

# class Referee(db.Model):
#     first_name = db.Column(db.String(128), nullable=False)
#     last_name = db.Column(db.String(128), nullable=False)
#     last_name = db.Column(db.String(128), nullable=False)