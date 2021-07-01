from flask import Blueprint, jsonify, render_template, request
import requests

ui_divisions_blueprint = Blueprint('divisions', __name__, template_folder='./templates')

# TODO navbar dropdown menu
# TODO when two teams have the same amount of points you need to look at which team has a higher GD
@ui_divisions_blueprint.route('/divisions/overview/<division_id>', methods=['GET'])
def show_team_overview(division_id):
    division = requests.get(f'http://leagues:5000/divisions/{division_id}').json()
    matches_by_week = dict()
    extra_info = dict()  # used to store information needed in the "Rangschikking" table
    team_rankings = dict()  # used to store information needed in the "Rangschikking" table
    for i in range(1, requests.get(f'http://leagues:5000/matches/matchweek/max').json()['max']):
        # get matches from a matchweek within the division
        matches = requests.get(f'http://leagues:5000/matches/division/{division_id}/matchweek/{i}').json()
        matches_by_week[i] = matches
        # calculate extra information needed
        for match in matches:
            team_id = match['home_team_id']
            if team_id not in extra_info:
                team_name_full = requests.get(f'http://teams:5000/teams/full-team-name/{team_id}').json()
                extra_info[team_id] ={'full_name': team_name_full, 'played': 0, 'wun': 0, 'lost': 0, 'equal': 0, 'goals_for': 0, 'goals_against': 0}
            # update extra info
            if match['goals_home_team'] is not None:
                extra_info[team_id]['played'] += 1
            else:
                continue  # match is not played yet
            if match['goals_home_team'] > match['goals_away_team']:
                extra_info[team_id]['wun'] += 1
            elif match['goals_home_team'] < match['goals_away_team']:
                extra_info[team_id]['lost'] += 1
            else:
                extra_info[team_id]['equal'] += 1
            extra_info[team_id]['goals_for'] += match['goals_home_team']
            extra_info[team_id]['goals_against'] += match['goals_away_team']
            # add points
            team_rankings.setdefault(team_id, 0)
            if match['goals_home_team'] > match['goals_away_team']:
                team_rankings[team_id] += 3  # home team wins
            elif match['goals_home_team'] == match['goals_away_team']:
                team_rankings[team_id] += 1  # equal
    # calculate team rankings
    team_rankings = sorted(team_rankings.items(), key=lambda x: x[1], reverse=True)

    return render_template("division_overview_single.html", division=division, matches_by_week=matches_by_week,
                           team_rankings=team_rankings, extra_info=extra_info)

@ui_divisions_blueprint.route('/divisions/overview', methods=['GET'])
def show_all_teams():
    response = requests.get(f'http://teams:5000/teams/all').json()
    return render_template("all_teams_overview.html", teams=response)
