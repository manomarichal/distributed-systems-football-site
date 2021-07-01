from flask import Blueprint, jsonify, render_template, request
import requests
import datetime as dt

ui_teams_blueprint = Blueprint('teams', __name__, template_folder='./templates')

@ui_teams_blueprint.route('/teams/overview/<team_id>', methods=['GET'])
def show_team_overview(team_id):
    team = requests.get("http://teams:5000/teams/%s"%team_id).json()
    extra_info = dict()
    extra_info['club'] = requests.get("http://teams:5000/clubs/%d"%team['stam_id']).json()['name']
    extra_info['full_name'] = requests.get("http://teams:5000/teams/full-team-name/%s"%team_id).json()

    # find upcoming and three most recent matches
    matches = requests.get("http://leagues:5000/leagues/matches/?home_team_id=%s"%team_id).json()
    upcoming_matches = dict()
    played_matches = dict()
    for match in matches:
        # check if match is played already
        if match['goals_home_team'] is None:
            upcoming_matches[match['id']] = match
        else:
            played_matches[match['id']] = match
    # sort
    return render_template("teams_overview_single.html", team = team, extra_info = extra_info)

# TODO make this page faster
@ui_teams_blueprint.route('/teams/overview', methods=['GET'])
def show_all_teams():
    teams = requests.get(f'http://teams:5000/teams').json()
    extra_info = dict()
    for team in teams:
        full_name = requests.get("http://teams:5000/teams/full-team-name/%d"%team['id']).json()
        club = requests.get("http://teams:5000/clubs/%d"%team['stam_id']).json()['name']
        extra_info[team['id']] = {'full_name': full_name, 'club':club}
    return render_template("teams_overview_all.html", teams = teams, extra_info=extra_info)