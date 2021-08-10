from sqlalchemy.sql import func
from project import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    def __init__(self, username, password, team_id, admin):
        self.username = username
        self.password = password
        self.team_id = team_id if team_id != "None" else None
        self.admin = admin

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))