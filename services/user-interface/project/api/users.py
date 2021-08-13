from project import db
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from project.api.models import User
from project.api.forms import LoginForm, ScoreForm, ClubForm, TeamForm, NewRefereeForm
import requests
import json


ui_users_blueprint = Blueprint('users', __name__, template_folder='./templates')

@ui_users_blueprint.route('/user/team-portal', methods=['GET'])
@login_required
def team_portal():
    if current_user.team_id == None:
        return render_template("not_authorized.html"), 404
    id = current_user.team_id
    form = ClubForm()
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    try:
        club = requests.get("http://teams:5000/teams/%s/club" % id).json()
        team = requests.get("http://teams:5000/teams/%s" % id).json()
        matches = requests.get("http://leagues:5000/matches/home-team/%s" % id).json()
        return render_template("team_portal.html", id=id, team=team, matches=matches, full_names=full_names, form=form, club=club)
    except Exception:
        return render_template("internal_server_error.html"), 500

@ui_users_blueprint.route('/user/match/<match_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_game_score(match_id):
    if current_user.team_id == None:
        return render_template("not_authorized.html"), 404
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
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/club/edit', methods=['GET', 'POST'])
@login_required
def edit_club_info():
    if current_user.team_id == None:
        return render_template("not_authorized.html"), 404
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
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/team/edit', methods=['GET', 'POST'])
@login_required
def edit_team_info():
    if current_user.team_id == None:
        return render_template("not_authorized.html"), 404
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
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/admin', methods=['GET', 'POST'])
@login_required
def show_admin():
    if current_user.admin != True and current_user.super_admin != True:
        return render_template("not_authorized.html"), 404
    try:
        return render_template("admin_interface.html")
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/admin/referees/assign', methods=['GET', 'POST'])
@login_required
def referee_overview():
    if current_user.admin != True and current_user.super_admin != True:
        return render_template("not_authorized.html"), 404
    try:
        matches_by_week = requests.get("http://leagues:5000/matches/per-week").json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        referee_names = requests.get("http://referees:5000/referees/names").json()
        return render_template("admin_assign_referees.html", full_names=full_names, matches_by_week=matches_by_week, referee_names=referee_names)
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/match/<match_id>/referee', methods=['GET'])
@login_required
def assign_referee_to_match(match_id):
    if current_user.admin != True and current_user.super_admin != True:
        return render_template("not_authorized.html"), 404
    try:
        referees = requests.get("http://referees:5000/referees").json()
        match = requests.get("http://leagues:5000/matches/%s" % match_id).json()
        unavailable_referee_ids = requests.get("http://leagues:5000/matches/matchweek/%s/referees/assigned" % match["matchweek"]).json()
        referee_names = requests.get("http://referees:5000/referees/names").json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()

        available_referees = list()
        unavailable_referees = list()
        for referee in referees:
            if referee["id"] in unavailable_referee_ids["referee_ids"]:
                unavailable_referees.append(referee)
            else:
                available_referees.append(referee)
        return render_template("edit_match_referee.html", referee_names=referee_names, available_referees=available_referees, unavailable_referees=unavailable_referees ,full_names=full_names, match=match)
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/match/<match_id>/referee', methods=['POST'])
@login_required
def update_match_referee(match_id):
    if current_user.admin != True and current_user.super_admin != True:
        return render_template("not_authorized.html"), 404
    try:
        requests.post("http://leagues:5000/matches/%s/referee" % match_id, json=request.form)
        return redirect(url_for('users.referee_overview'))
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/super-admin/permissions', methods=['GET'])
@login_required
def update_admins_interface():
    if current_user.super_admin != True :
        return render_template("not_authorized.html"), 404
    try:
        users = db.session.query(User).order_by(User.username)
        return render_template("admin_superadmin_interface.html", users=users)
    except Exception:
        return render_template("internal_server_error.html"), 500


@ui_users_blueprint.route('/user/super-admin/permissions', methods=['POST'])
@login_required
def update_admins():
    try:
        data = request.form
        if data.get("remove_admin"):
            user = User.query.filter_by(id=data.get("remove_admin")).first()
            user.admin = False
        elif data.get("make_admin"):
            user = User.query.filter_by(id=data.get("make_admin")).first()
            user.admin = True
        db.session.commit()
        return redirect(url_for("users.update_admins_interface"))
    except Exception:
        return render_template("internal_server_error.html"), 500