from flask import Blueprint, jsonify
from project.api.models import Referee
import json

referees_blueprint = Blueprint('referees', __name__)

@referees_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@referees_blueprint.route('/referees/<referee_id>', methods=['GET'])
def get_referee_by_id(referee_id):
    fail = {'status': 'fail',
            'message': 'Team does not exist'}
    try:
        result = Referee.query.filter_by(id=referee_id).first()
        if not result:
            return jsonify(fail), 404
        response = {
            'status': 'succes',
            'data': {
                'first_name' : result.first_name,
                'last_name' : result.last_name,
                'address' : result.address,
                'zip_code' : result.zip_code,
                'city' : result.city,
                'phone_number' : result.phone_number,
                'email' : result.email,
                'date_of_birth' : result.date_of_birth
            }
        }
        return jsonify(response), 200
    except ValueError:
        return jsonify(fail), 404

@referees_blueprint.route('/referees', methods=['GET'])
def get_available_referees():
    result = Referee.query.all()
    return json.dumps([row.to_dict() for row in result]), 200