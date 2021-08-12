from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ScoreForm(FlaskForm):
    home_score = IntegerField('Goals thuisploeg', validators=[NumberRange(min=0)])
    away_score = IntegerField('Goals uitploeg', validators=[NumberRange(min=0)])
    submit = SubmitField('Bevestig')

class ClubForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    zip_code = IntegerField('Zip code', validators=[DataRequired()])
    city = StringField('Stad', validators=[DataRequired()])
    website = StringField('Website')
    submit = SubmitField('Bevestig')

class TeamForm(FlaskForm):
    colors = StringField('Kleuren', validators=[DataRequired()])
    suffix = StringField('suffix', validators=[DataRequired()])
    stam_id = IntegerField('Stam id', validators=[DataRequired()])
    submit = SubmitField('Bevestig')

class NewRefereeForm(FlaskForm):
    new_id = IntegerField('referee id', validators=[DataRequired()])