import json
from flask_login import current_user, login_required
from flask import Blueprint, jsonify, render_template, request
import requests

ui_matches_blueprint = Blueprint('matches', __name__, template_folder='./templates')
@ui_matches_blueprint.route('/matches/<match_id>/overview', methods=['GET'])
def show_match_overview(match_id):
    try:
        API_KEY = "8d225f3be378ce1b356c39b0810dc696"
        match = requests.get("http://leagues:5000/matches/%s"%match_id).json()
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        home_team_tr = requests.get("http://leagues:5000/matches/track-record/%s"%match["home_team_id"]).text
        away_team_tr = requests.get("http://leagues:5000/matches/track-record/%s"%match["away_team_id"]).text
        statistics = requests.get("http://leagues:5000/matches/statistics/%s/vs/%s"%(match["home_team_id"], match["away_team_id"])).json()
        prev_matches = requests.get("http://leagues:5000/matches/%s/vs/%s"%(match["home_team_id"], match["away_team_id"])).json()

        home_team_adress = requests.get("http://teams:5000/teams/%s/address"%(match["home_team_id"])).json()
    except Exception:
        return render_template("internal_server_error.html"), 500

    # weather
    try:
        weather = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=51.21989&lon=4.40346&exclude=current,minutely,hourly,alerts&appid=" + API_KEY).json()
        return render_template("match_overview.html", weather=weather, match=match, full_names=full_names,
                               home_team_track_record=home_team_tr, away_team_track_record=away_team_tr,
                               statistics=statistics, prev_matches=prev_matches, address=home_team_adress)
    except requests.exceptions.ConnectionError:
        return render_template("match_overview_no_weather.html", match=match, full_names=full_names,
                               home_team_track_record=home_team_tr, away_team_track_record=away_team_tr,
                               statistics=statistics, prev_matches=prev_matches, address=home_team_adress)
    except Exception:
        return render_template("internal_server_error.html"), 500

@ui_matches_blueprint.route('/user/super-admin/logins', methods=['GET'])
@login_required
def generate_logins():
    if current_user.super_admin != True :
        return render_template("not_authorized.html"), 404
    full_names = requests.get("http://teams:5000/teams/full-names").json()
    file = open("./logins.csv", "w")
    for name_id in full_names:
        file.write(full_names[name_id].replace(" ", "") + ",password," + name_id +",False,False\n")
    file.close()
    return "success"






