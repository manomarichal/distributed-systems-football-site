from flask import Blueprint, jsonify
from project.api.models import Club

clubs_blueprint = Blueprint('clubs', __name__)

@clubs_blueprint.route('/clubs/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@clubs_blueprint.route('/clubs/<name>', methods=['GET'])
def get_user_by_id(name):
    fail = {'status': 'fail',
            'message': 'Club does not exist'}
    try:
        result = Club.query.filter_by(id=name).first()
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