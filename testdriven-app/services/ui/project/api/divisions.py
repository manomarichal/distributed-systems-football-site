from flask import Blueprint, jsonify, render_template, request
import requests

ui_divisions_blueprint = Blueprint('divisions', __name__, template_folder='./templates')


# TODO navbar dropdown menu
# TODO when two teams have the same amount of points you need to look at which team has a higher GD
@ui_divisions_blueprint.route('/divisions/overview/<division_id>', methods=['GET', 'POST'])
def show_team_overview(division_id):
    division = requests.get("http://leagues:5000/divisions/%s"%division_id).json()
    full_names = requests.get("http://teams:5000/teams/full-names").json()

    matches_by_week = requests.get("http://leagues:5000/matches/division/%s/per-week"%division_id).json()
    statistics = requests.get("http://leagues:5000/matches/division/%s/statistics"%division_id).json()

    best_attack = requests.get(f'http://leagues:5000/matches/division/{division_id}/best-attack').json()
    best_defense = requests.get(f'http://leagues:5000/matches/division/{division_id}/best-defense').json()
    most_clean_sheets = requests.get(f'http://leagues:5000/matches/division/{division_id}/most-clean-sheets').json()

    team_points = requests.get("http://leagues:5000/matches/division/%s/team-points"%division_id).json()
    team_rankings = sorted(team_points.items(), key=lambda x: x[1], reverse=True)

    return render_template("division_overview_single.html", division=division, matches_by_week=matches_by_week,
                           full_names=full_names,
                           team_rankings=team_rankings, statistics=statistics, best_attack=best_attack,
                           best_defense=best_defense, most_clean_sheets=most_clean_sheets)


@ui_divisions_blueprint.route('/divisions/overview', methods=['GET'])
def show_all_teams():
    response = requests.get(f'http://teams:5000/teams/all').json()
    return render_template("all_teams_overview.html", teams=response)
