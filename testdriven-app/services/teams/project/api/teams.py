from flask import Blueprint, jsonify, request
from project.api.models import Team, Club
from project import db
import json

teams_blueprint = Blueprint('teams', __name__)

@teams_blueprint.route('/teams/<team_id>', methods=['GET'])
def get_team_info(team_id):
    try:
        result = Team.query.filter_by(id=team_id).first()
        if not result:
            return jsonify({'status': 'fail','message': 'Team does not exist'}), 404
        return json.dumps(result.to_dict()), 200
    except ValueError:
        return jsonify({'status': 'fail','message': 'Team does not exist'}), 404

@teams_blueprint.route('/teams/<team_id>/address', methods=['GET'])
def get_team_adress(team_id):
    try:
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'status': 'fail', 'message': 'Team does not exist'}), 404

        club = Club.query.filter_by(stam_id=team.stam_id).first()
        return jsonify({'city': club.city, 'zip_code': club.zip_code, 'address': club.address}), 404
    except ValueError:
        return jsonify({'status': 'fail','message': 'Team does not exist'}), 404

@teams_blueprint.route('/teams/<team_id>/club', methods=['GET'])
def get_club_from_team_id(team_id):
    try:
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'status': 'fail', 'message': 'Team does not exist'}), 404

        club = Club.query.filter_by(stam_id=team.stam_id).first()
        return json.dumps(club.to_dict())
    except ValueError:
        return jsonify({'status': 'fail','message': 'Team does not exist'}), 404

@teams_blueprint.route('/teams/<team_id>/full-name', methods=['GET'])
def get_team_name_by_id(team_id):
    try:
        team_object = Team.query.filter_by(id=team_id).first().to_dict()
        club_object = Club.query.filter_by(stam_id=team_object['stam_id']).first().to_dict()
        if not team_object:
            return jsonify({'status': 'fail','message': 'Team does not exist'}), 404
        if not club_object:
            return jsonify({'status': 'fail','message': 'Club does not exist'})
        return json.dumps(club_object['name'] + ' ' + team_object['suffix']), 200
    except ValueError:
        return jsonify({'status': 'fail','message': 'Team or club does not exist'}), 404

@teams_blueprint.route('/teams/full-names', methods=['GET'])
def get_all_team_names():
    names = dict()
    teams = Team.query.all()
    for team in teams:
        names[team.id] = db.session.query(Club).filter_by(stam_id=team.stam_id).first().name + ' ' + team.suffix
    return jsonify(names), 200

@teams_blueprint.route('/teams', methods=['GET'])
def get_all_teams():
    result = Team.query.all()
    return json.dumps([row.to_dict() for row in result]), 200

@teams_blueprint.route('/clubs/<stam_number>', methods=['GET'])
def get_club_by_stam_number(stam_number):
    try:
        result = Club.query.filter_by(stam_id=stam_number).first()
        if not result:
            return jsonify({'status': 'fail','message': 'Club does not exist'}), 404
        return json.dumps(result.to_dict()), 200
    except ValueError:
        return jsonify({'status': 'fail','message': 'Club does not exist'}), 404

### PUT REQUESTS ###
@teams_blueprint.route('/teams/<team_id>/club', methods=['PUT'])
def update_club_info(team_id):
    try:
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'status': 'fail', 'message': 'Team does not exist'}), 404

        club = Club.query.filter_by(stam_id=team.stam_id).first()
        data = request.get_json()
        club.name = data.get("name")
        club.address = data.get("address")
        club.city = data.get("city")
        club.zip_code = int(data.get("zip_code"))
        club.website = data.get("website")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return jsonify({'status': 'fail','message': 'Failed'}), 406
    return jsonify({'status' : 'succes'}), 200

@teams_blueprint.route('/teams/<team_id>', methods=['PUT'])
def update_team_info(team_id):
    try:
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'status': 'fail', 'message': 'Team does not exist'}), 404

        data = request.get_json()
        team.colors = data.get("colors")
        team.suffix = data.get("suffix")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return jsonify({'status': 'fail','message': 'Failed'}), 406
    return jsonify({'status' : 'succes'}), 200
