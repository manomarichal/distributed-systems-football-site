from flask import Blueprint, jsonify, request
from project.api.models import Division
from project import db
from sqlalchemy import func
import json

divisions_blueprint = Blueprint('divisions', __name__)
@divisions_blueprint.route('/divisions/<division_id>', methods=['GET'])
def get_division_by_division_id(division_id):
    try:
        result = Division.query.filter_by(id=division_id).first()
        if not result:
            return jsonify({'status': 'fail','message': 'Division does not exist'}), 404
        return json.dumps(result.to_dict())
    except ValueError:
        return jsonify({'status': 'fail','message': 'Division does not exist'}), 404

@divisions_blueprint.route('/divisions/', methods=['GET'])
def get_all_divisions():
    result = Division.query.all()
    return json.dumps([row.to_dict() for row in result]), 200
