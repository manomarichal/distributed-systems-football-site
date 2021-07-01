from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Team, Club
import csv

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def add_teams_data():
    try:
        with open('data/teams.csv', mode='r')as file:
            data = csv.reader(file)
            for row ,line in enumerate(data):
                if row == 0: continue
                db.session.add(Team(id=line[0],
                                    stam_id=line[1],
                                    suffix=line[2],
                                    colors=line[3]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))

@cli.command()
def add_clubs_data():
    try:
        with open('data/clubs.csv', mode='r')as file:
            data = csv.reader(file)
            for row ,line in enumerate(data):
                if row == 0: continue
                db.session.add(Club(stam_id=line[0],
                                    name=line[1],
                                    address=line[2],
                                    zip_code=line[3],
                                    city=line[4],
                                    website=line[5]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))

if __name__ == '__main__':
    cli()