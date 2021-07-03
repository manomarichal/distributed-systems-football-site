from flask import Blueprint, jsonify, request
from project.api.models import Match
from project import db
from sqlalchemy import func
import json

matches_blueprint = Blueprint('matches', __name__)

@matches_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@matches_blueprint.route('/matches/division/<division_id>/matchweek/<matchweek_nr>', methods=['GET'])
def get_specific_matches(division_id, matchweek_nr):
    result = Match.query.filter_by(division_id=division_id, matchweek=matchweek_nr)
    return json.dumps([row.to_dict() for row in result]), 200

@matches_blueprint.route('/matches/matchweek/max', methods=['GET'])
def get_max_matchweeks():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200

@matches_blueprint.route('/matches/division/<division_id>/best-attack', methods=['GET'])
def get_team_with_best_attack(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict=dict()
    for row in matches:
        score_dict.setdefault(row.home_team_id, 0)
        if row.goals_home_team is not None:
            score_dict[row.home_team_id] += row.goals_home_team

    max_key = max(score_dict, key=score_dict.get)
    return json.dumps({'team' : max_key, 'goals': score_dict[max_key]})

@matches_blueprint.route('/matches/division/<division_id>/best-defense', methods=['GET'])
def get_team_with_best_defense(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict=dict()
    for row in matches:
        if row.goals_away_team is not None:
            score_dict.setdefault(row.home_team_id, 0)
            score_dict[row.home_team_id] += row.goals_away_team

    min_key = min(score_dict, key=score_dict.get)
    return json.dumps({'team' : min_key, 'goals': score_dict[min_key]})

@matches_blueprint.route('/matches/division/<division_id>/most-clean-sheets', methods=['GET'])
def get_team_with_most_clean_sheets(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict=dict()
    for row in matches:
        if row.goals_home_team == 0:
            score_dict.setdefault(row.home_team_id, 0)
            score_dict[row.home_team_id] += 1
        if row.goals_away_team == 0:
            score_dict.setdefault(row.away_team_id, 0)
            score_dict[row.away_team_id] += 1

    max_key = max(score_dict, key=score_dict.get)
    return json.dumps({'team' : max_key, 'nr_of_clean_sheets': score_dict[max_key]})

@matches_blueprint.route('/matches/home-team/recent', methods=['GET'])
def get_upcoming_matches_for_team():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200