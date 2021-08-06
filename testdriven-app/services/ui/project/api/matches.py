import json

from flask import Blueprint, jsonify, render_template, request
import requests

ui_matches_blueprint = Blueprint('matches', __name__, template_folder='./templates')
@ui_matches_blueprint.route('/matches/overview/<match_id>', methods=['GET'])
# TODO true locations instead of fixed locations
def show_match_overview(match_id):
    API_KEY = "15d10c8df5b3bf6c4e339868db4a999f"
    match = requests.get("http://leagues:5000/matches/%s"%match_id).json()
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    home_team_tr = requests.get("http://leagues:5000/matches/track-record/%s"%match["home_team_id"]).text
    away_team_tr = requests.get("http://leagues:5000/matches/track-record/%s"%match["away_team_id"]).text
    statistics = requests.get("http://leagues:5000/matches/statistics/%s/vs/%s"%(match["home_team_id"], match["away_team_id"])).json()
    prev_matches = requests.get("http://leagues:5000/matches/%s/vs/%s"%(match["home_team_id"], match["away_team_id"])).json()

    home_team_adress = requests.get("http://teams:5000/teams/address/%s"%(match["home_team_id"])).json()

    # weather
    try:
        weather = requests.get(f'http://api.openweathermap.org/data/2.5/onecall?lat={51.21989}&lon={4.40346}&exclude=current,minutely,hourly,alerts&appid={API_KEY}').json()
        return render_template("match_overview.html", weather=weather, match=match, full_names=full_names,
                               home_team_track_record=home_team_tr, away_team_track_record=away_team_tr,
                               statistics=statistics, prev_matches=prev_matches, address=home_team_adress)
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'api.openweathermap.org is refusing the connection'}), 404






