import json

from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from project.api.models import User
from project.api.forms import LoginForm, ScoreForm, ClubForm, TeamForm
import requests


ui_users_blueprint = Blueprint('users', __name__, template_folder='./templates')

@ui_users_blueprint.route('/user/team-portal', methods=['GET'])
@login_required
def team_portal():
    id = current_user.team_id
    form = ClubForm()
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    try:
        club = requests.get("http://teams:5000/teams/%s/club" % id).json()
        team = requests.get("http://teams:5000/teams/%s" % id).json()
        matches = requests.get("http://leagues:5000/matches/home-team/%s" % id).json()
        return render_template("team_portal.html", id=id, team=team, matches=matches, full_names=full_names, form=form, club=club)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404

@ui_users_blueprint.route('/user/edit-match/<match_id>', methods=['GET', 'POST'])
@login_required
def edit_game_score(match_id):
    session.pop('_flashes', None)
    form = ScoreForm()
    if form.validate_on_submit():
        requests.put("http://leagues:5000/matches/%s/score" % match_id, json=request.form.to_dict())
        return redirect(url_for('users.team_portal'))
    else:
        # session.pop('_flashes', None)
        # flash('Vul beide velden met een getal in')
        pass
    try:
        match = requests.get("http://leagues:5000/matches/%s" % match_id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        return render_template("edit_match_score.html", match=match, full_names=full_names, form=form)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404


@ui_users_blueprint.route('/user/edit-club-info', methods=['GET', 'POST'])
@login_required
def edit_club_info():
    form = ClubForm()
    id = current_user.team_id
    if form.validate_on_submit():
        requests.put("http://teams:5000/teams/%s/club" % id, json=request.form.to_dict())
        return redirect(url_for('users.team_portal'))
    else:
        pass
    try:
        team = requests.get("http://teams:5000/teams/%s" % id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        club = requests.get("http://teams:5000/teams/%s/club" % id).json()
        return render_template("edit_club_info.html", id=id, team=team, full_names=full_names, form=form, club=club)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404

@ui_users_blueprint.route('/user/edit-team-info', methods=['GET', 'POST'])
@login_required
def edit_team_info():
    form = TeamForm()
    id = current_user.team_id
    if form.validate_on_submit():
        requests.put("http://teams:5000/teams/%s" % id, json=request.form.to_dict())
        return redirect(url_for('users.team_portal'))
    else:
        pass
    try:
        team = requests.get("http://teams:5000/teams/%s" % id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        return render_template("edit_team_info.html", id=id, team=team, full_names=full_names, form=form)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'service required by this route is down'}), 404

