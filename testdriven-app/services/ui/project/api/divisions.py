from flask import Blueprint, jsonify, render_template, request
import requests

ui_divisions_blueprint = Blueprint('divisions', __name__, template_folder='./templates')

@ui_divisions_blueprint.route('/divisions/overview/<division_id>', methods=['GET'])
def show_team_overview(division_id):
    division = requests.get(f'http://leagues:5000/leagues/divisions/{division_id}').json()
    matches_by_week = dict()
    for i in range(1, requests.get(f'http://leagues:5000/leagues/matchweeks/max').json()['max']):
        matches_by_week[i] = requests.get(f'http://leagues:5000/leagues/matches/?matchweek={i}&div_id={division_id}').json()
    return render_template("division_overview_single.html", division = division, matches_by_week = matches_by_week)

@ui_divisions_blueprint.route('/divisions/overview', methods=['GET'])
def show_all_teams():
    response = requests.get(f'http://teams:5000/teams/all').json()
    return render_template("all_teams_overview.html", teams = response)