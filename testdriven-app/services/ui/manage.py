from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User
import csv

cli = FlaskGroup(create_app=create_app)  # new

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def add_user_data():
    try:
        with open('data/team_users.csv', mode='r')as file:
            data = csv.reader(file)
            for row ,line in enumerate(data):
                if row == 0 or len(line) != 4: continue
                db.session.add(User(username=line[0],
                                    password=line[1],
                                    team_id=line[2],
                                    admin=True if line[3] == "True" else False))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))


if __name__ == '__main__':
    cli()