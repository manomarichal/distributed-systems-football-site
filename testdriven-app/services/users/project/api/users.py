from flask import Blueprint, jsonify
from project.api.models import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'    })

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    fail = {'status': 'fail',
            'message': 'User does not exist'}
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(fail), 404

        response = {
            'status': 'succes',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'active': user.active,
            }
        }
        return jsonify(response), 200
    except ValueError:
        return jsonify(fail), 404