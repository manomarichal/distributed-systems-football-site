from flask import Blueprint, jsonify
from project.api.models import Match, Division
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

@leagues_blueprint.route('/leagues/matches', methods=['GET'])
def get_all_matches():
    result = Match.query.all()
    return json.dumps([row.to_dict() for row in result]), 200

@leagues_blueprint.route('/leagues/divisions/<division_id>', methods=['GET'])
def get_division_by_division_id(division_id):
    fail = {'status': 'fail','message': 'Team does not exist'}
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