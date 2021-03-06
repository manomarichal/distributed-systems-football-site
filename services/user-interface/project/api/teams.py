from flask import Blueprint, jsonify, render_template, request
import requests
import datetime as dt

ui_teams_blueprint = Blueprint('teams', __name__, template_folder='./templates')

@ui_teams_blueprint.route('/teams/<team_id>', methods=['GET'])
def show_team_overview(team_id):
    try:
        team = requests.get("http://teams:5000/teams/%s"%team_id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        upcoming_matches = requests.get("http://leagues:5000/matches/home-team/%s/upcoming"%team_id).json()
        recent_matches = requests.get("http://leagues:5000/matches/home-team/%s/recent"%team_id).json()

        extra_info = dict()
        extra_info['club'] = requests.get("http://teams:5000/clubs/%d"%team['stam_id']).json()['name']
        extra_info['full_name'] = requests.get("http://teams:5000/teams/%s/full-name"%team_id).json()

        return render_template("teams_overview_single.html", team = team, extra_info = extra_info, recent_matches=recent_matches, upcoming_matches=upcoming_matches, full_names = full_names)
    except Exception:
        return render_template("internal_server_error.html"), 500

@ui_teams_blueprint.route('/teams', methods=['GET'])
def show_all_teams():
    try:
        teams = requests.get(f'http://teams:5000/teams').json()
        extra_info = dict()
        for team in teams:
            full_name = requests.get("http://teams:5000/teams/%d/full-name"%team['id']).json()
            club = requests.get("http://teams:5000/clubs/%d"%team['stam_id']).json()['name']
            extra_info[team['id']] = {'full_name': full_name, 'club':club}
        return render_template("teams_overview_all.html", teams = teams, extra_info=extra_info)
    except Exception:
        return render_template("internal_server_error.html"), 500