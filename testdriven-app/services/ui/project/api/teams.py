from flask import Blueprint, jsonify, render_template, request
import requests

ui_teams_blueprint = Blueprint('teams', __name__, template_folder='./templates')

@ui_teams_blueprint.route('/teams/overview/<team_id>', methods=['GET'])
def show_team_overview(team_id):
    response = requests.get(f'http://teams:5000/teams/{team_id}').json()
    return render_template("teams_overview_single.html", team = response)

@ui_teams_blueprint.route('/teams/overview', methods=['GET'])
def show_all_teams():
    response = requests.get(f'http://teams:5000/teams/all').json()
    return render_template("teams_overview_all.html", teams = response)