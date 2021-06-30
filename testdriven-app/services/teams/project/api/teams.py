from flask import Blueprint, jsonify
from project.api.models import Team
import json

teams_blueprint = Blueprint('teams', __name__)

@teams_blueprint.route('/teams/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@teams_blueprint.route('/teams/<team_id>', methods=['GET'])
def get_user_by_id(team_id):
    fail = {'status': 'fail','message': 'Team does not exist'}
    try:
        result = Team.query.filter_by(id=team_id).first()
        if not result:
            return jsonify(fail), 404
        return json.dumps(result.to_dict())
    except ValueError:
        return jsonify(fail), 404

@teams_blueprint.route('/teams/all', methods=['GET'])
def get_all_teams():
    result = Team.query.all()
    return json.dumps([row.to_dict() for row in result]), 200

# @teams_blueprint.route('/teams/names', methods=['GET'])
# def get_name_teams():
#     result = Team.query.with_entities(Team.id, Team.col2)
#     return json.dumps([row.to_dict() for row in result]), 200
