from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Referee
import csv

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def add_referees_data():
    try:
        with open('data/referees.csv', mode='r')as file:
            data = csv.reader(file)
            for row ,line in enumerate(data):
                if row == 0: continue
                db.session.add(Referee(first_name=line[0],
                                    last_name=line[1],
                                    address=line[2],
                                    zip_code=line[3],
                                    city=line[4],
                                    phone_number=line[5],
                                    email=line[6],
                                    date_of_birth=line[7]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))



if __name__ == '__main__':
    cli()