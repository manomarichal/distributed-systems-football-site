from flask import Blueprint, jsonify
from project.api.models import Team

teams_blueprint = Blueprint('teams', __name__)

@teams_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@teams_blueprint.route('/teams/<team_id>', methods=['GET'])
def get_user_by_id(team_id):
    fail = {'status': 'fail',
            'message': 'Team does not exist'}
    try:
        result = Team.query.filter_by(id=team_id).first()
        if not result:
            return jsonify(fail), 404
        response = {
            'status': 'succes',
            'data': {
                'id': result.id,
                'stam_id': result.stam_id,
                'suffix': result.suffix,
                'colors': result.colors,
            }
        }
        return jsonify(response), 200
    except ValueError:
        return jsonify(fail), 404