from flask import Blueprint, jsonify, request
from project.api.models import Match
from project import db
from sqlalchemy import func
import json

matches_blueprint = Blueprint('matches', __name__)

@matches_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

# TODO find better way todo this
@matches_blueprint.route('/matches/division/<division_id>/matchweek/<matchweek_nr>', methods=['GET'])
def get_specific_matches(division_id, matchweek_nr):
    result = Match.query.filter_by(division_id=division_id, matchweek=matchweek_nr)
    return json.dumps([row.to_dict() for row in result]), 200

@matches_blueprint.route('/matches/matchweek/max', methods=['GET'])
def get_max_matchweeks():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200

@matches_blueprint.route('/matches/home-team/recent', methods=['GET'])
def get_upcoming_matches_for_team():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200