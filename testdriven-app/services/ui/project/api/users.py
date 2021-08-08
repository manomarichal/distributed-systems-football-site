import json

from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from project.api.models import User
from project.api.forms import LoginForm, ScoreForm
import requests


ui_users_blueprint = Blueprint('users', __name__, template_folder='./templates')

@ui_users_blueprint.route('/user/edit-scores', methods=['GET'])
@login_required
def edit_scores():
    id = current_user.team_id
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    try:
        matches = requests.get("http://leagues:5000/matches/home-team/%s" % id).json()
        return render_template("edit_match_scores.html", id=id, matches=matches, full_names=full_names)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404

@ui_users_blueprint.route('/user/edit-scores/<match_id>', methods=['GET', 'POST'])
@login_required
def edit_game_score(match_id):
    session.pop('_flashes', None)
    form = ScoreForm()
    if form.validate_on_submit():
        # flash('Update score succesvol') # TODO flashes
        return redirect(url_for('users.edit_scores'))
    else:
        # session.pop('_flashes', None)
        # flash('Vul beide velden met een getal in')
        pass
    try:
        match = requests.get("http://leagues:5000/matches/%s" % match_id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        return render_template("edit_match_scores_single.html", match=match, full_names=full_names, form=form)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404