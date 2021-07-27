from flask import Blueprint, jsonify, render_template, request
import requests

ui_matches_blueprint = Blueprint('matches', __name__, template_folder='./templates')
@ui_matches_blueprint.route('/matches/overview/<match_id>', methods=['GET', 'POST'])
def show_match_overview(match_id):
    match = requests.get("http://leagues:5000/matches/%s"%match_id).json()
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    home_team_track_record = requests.get("http://leagues:5000/matches/track-record/%s"%match["home_team_id"]).json()
    away_team_track_record = requests.get("http://leagues:5000/matches/track-record/%s"%match.away_team_id).json()
    statistics = requests.get("http://leagues:5000/matches/%s/vs/%s/"%(match.home_team_id, match.away_team_id)).json()
    return render_template("match_overview.html", match = match, full_names = full_names)




