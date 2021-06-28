from flask import Blueprint, jsonify, render_template, request
import requests

ui_divisions_blueprint = Blueprint('divisions', __name__, template_folder='./templates')

@ui_divisions_blueprint.route('/divisions/overview/<team_id>', methods=['GET'])
def show_team_overview(team_id):
    response = requests.get(f'http://teams:5000/teams/{team_id}').json()
    return render_template("single_team_overview.html", team = response)

@ui_divisions_blueprint.route('/divisions/overview', methods=['GET'])
def show_all_teams():
    response = requests.get(f'http://teams:5000/teams/all').json()
    return render_template("all_teams_overview.html", teams = response)