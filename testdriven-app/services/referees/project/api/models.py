from sqlalchemy.sql import func
from project import db

class Referee(db.Model):
    __tablename__ = 'referees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.String(128), nullable=False)

    def __init__(self, first_name, last_name, address, zip_code, city, phone_number, email, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.phone_number = phone_number
        self.email = email
        self.date_of_birth = date_of_birth
