from sqlalchemy.sql import func
from project import db
from sqlalchemy_serializer import SerializerMixin

class Status(db.Model, SerializerMixin):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(128), nullable=False)

    def __init__(self, id, status_name):
        self.id = id
        self.status_name = status_name

class Division(db.Model, SerializerMixin):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Match(db.Model, SerializerMixin):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    division_id = db.Column(db.Integer, nullable=False)
    matchweek = db.Column(db.Integer, nullable=False)
    home_team_id = db.Column(db.Integer, nullable=True)
    away_team_id = db.Column(db.Integer, nullable=True)
    goals_home_team = db.Column(db.Integer, nullable=True)
    goals_away_team = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    referee_id = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, division_id, matchweek, date, time, home_team_id, away_team_id, goals_home_team, goals_away_team, status):
        self.matchweek = matchweek
        self.division_id = division_id
        self.date = date
        self.time = time
        self.home_team_id = home_team_id if home_team_id != "NULL" else None
        self.away_team_id = away_team_id if away_team_id != "NULL" else None
        self.goals_home_team = goals_home_team if goals_home_team != "NULL" else None
        self.goals_away_team = goals_away_team if goals_away_team != "NULL" else None
        self.status = status if status != "NULL" else None
        self.referee_id = None
