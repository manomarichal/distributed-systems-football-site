from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Match, Division
import csv

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def add_matches_data():
    try:
        files = ['data/matches_2018_2019.csv', 'data/matches_2019_2020.csv', 'data/matches_2020_2021.csv']
        for filename in files:
            with open(filename, mode='r')as file:
                data = csv.reader(file)
                for row ,line in enumerate(data):
                    if row == 0: continue
                    db.session.add(Match(division_id=line[0],
                                         matchweek=line[1],
                                         date=line[2],
                                         time=line[3],
                                         home_team_id=line[4],
                                         away_team_id=line[5],
                                         goals_home_team=line[6],
                                         goals_away_team=line[7],
                                         status=line[8]))
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))

@cli.command()
def add_divisions_data():
    try:
        with open('data/divisions.csv', mode='r')as file:
            data = csv.reader(file)
            for row ,line in enumerate(data):
                if row == 0: continue
                db.session.add(Division(id=line[0],
                                    name=line[1]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))



if __name__ == '__main__':
    cli()