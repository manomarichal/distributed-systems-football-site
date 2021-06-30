from flask import Blueprint, jsonify, request
from project.api.models import Match, Division
from project import db
from sqlalchemy import func
import json

leagues_blueprint = Blueprint('leagues', __name__)

@leagues_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@leagues_blueprint.route('/leagues/matches/<team_id>', methods=['GET'])
def get_match_by_team_id(team_id):
    fail = {'status': 'fail','message': 'Team does not exist'}
    try:
        result = Match.query.filter_by(id=team_id).first()
        if not result:
            return jsonify(fail), 404
        return json.dumps(result.to_dict())
    except ValueError:
        return jsonify(fail), 404

@leagues_blueprint.route('/leagues/matches/matchweek/<week_nr>', methods=['GET'])
def get_matches_by_matchweek(week_nr):
    result = Match.query.filter(matchweek=week_nr)
    return json.dumps([row.to_dict() for row in result]), 200

# TODO find better way todo this
@leagues_blueprint.route('/leagues/matches/', methods=['GET'])
def get_specific_matches():
    arg_dict = request.args.to_dict()
    if 'div_id' in arg_dict and 'matchweek' in arg_dict:
        print('succes')
        result = Match.query.filter_by(division_id=arg_dict['div_id'], matchweek=arg_dict['matchweek'])
    else:
        result = Match.query.all()
    return json.dumps([row.to_dict() for row in result]), 200

@leagues_blueprint.route('/leagues/divisions/<division_id>', methods=['GET'])
def get_division_by_division_id(division_id):
    fail = {'status': 'fail','message': 'Division does not exist'}
    try:
        result = Division.query.filter_by(id=division_id).first()
        if not result:
            return jsonify(fail), 404
        return json.dumps(result.to_dict())
    except ValueError:
        return jsonify(fail), 404

@leagues_blueprint.route('/leagues/divisions', methods=['GET'])
def get_all_divisions():
    result = Division.query.all()
    return json.dumps([row.to_dict() for row in result]), 200

@leagues_blueprint.route('/leagues/matchweeks/max', methods=['GET'])
def get_max_matchweemks():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200