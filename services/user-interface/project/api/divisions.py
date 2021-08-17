from flask import Blueprint, jsonify, render_template, request
import requests

ui_divisions_blueprint = Blueprint('divisions', __name__, template_folder='./templates')

@ui_divisions_blueprint.route('/divisions/<division_id>', methods=['GET', 'POST'])
def show_team_overview(division_id):
    """"Page giving the league table, some statistics and upcoming fixtures for a given division"""

    try:
        full_names = requests.get("http://teams:5000/teams/full-names").json()
        status_names = requests.get("http://leagues:5000/status/full-names").json()
        division = requests.get("http://leagues:5000/divisions/%s" % division_id).json()
        matches_by_week = requests.get("http://leagues:5000/matches/division/%s/per-week" % division_id).json()
        statistics = requests.get("http://leagues:5000/matches/division/%s/statistics" % division_id).json()
        best_attack = requests.get("http://leagues:5000/matches/division/%s/best-attack" % division_id).json()
        best_defense = requests.get("http://leagues:5000/matches/division/%s/best-defense" % division_id).json()
        most_clean_sheets = requests.get("http://leagues:5000/matches/division/%s/most-clean-sheets" % division_id).json()
        team_points = requests.get("http://leagues:5000/matches/division/%s/team-points" % division_id).json()
        team_rankings = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
        return render_template("division_overview_single.html", division=division, matches_by_week=matches_by_week,
                               full_names=full_names,
                               team_rankings=team_rankings, statistics=statistics, best_attack=best_attack,
                               best_defense=best_defense, most_clean_sheets=most_clean_sheets, status_names=status_names)
    except Exception:
        return render_template("internal_server_error.html"), 500

@ui_divisions_blueprint.route('/divisions', methods=['GET'])
def show_all_divisions():
    try:
        divisions = requests.get("http://leagues:5000/divisions").json()
        return render_template("division_overview_all.html", divisions=divisions)
    except Exception:
        return render_template("internal_server_error.html"), 500

