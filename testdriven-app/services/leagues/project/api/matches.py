import datetime

import requests
from flask import Blueprint, jsonify, request
from project.api.models import Match
from project import db
from sqlalchemy import func, and_, or_, desc
import json

matches_blueprint = Blueprint('matches', __name__)

def sort_matches(matches):
    """Function to sort match objects"""
    matches = [row.to_dict() for row in matches]
    n = len(matches)
    format = "%Y-%m-%d %H:%M"
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            date_current = datetime.datetime.strptime(matches[j]["date"] + " " + matches[j]["time"], format)
            date_next = datetime.datetime.strptime(matches[j + 1]["date"] + " " + matches[j + 1]["time"], format)
            if date_current > date_next:
                matches[j], matches[j + 1] = matches[j + 1], matches[j]
                already_sorted = False
        if already_sorted:
            break
    return matches

### GET REQUESTS ###
@matches_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success', 'message': 'pong!'})


@matches_blueprint.route('/matches/home-team/<team_id>/recent', methods=['GET'])
def get_upcoming_matches_for_team(team_id):
    try:
        matches = Match.query.filter(and_(or_(Match.home_team_id == team_id, Match.away_team_id == team_id), Match.goals_home_team != None)).order_by(Match.date).all()
        matches = [row.to_dict() for row in reversed(matches)]
        return json.dumps(matches[0:3])
    except Exception:
        return jsonify({'status': 'fail','message': 'Operation failed'}), 404


@matches_blueprint.route('/matches/home-team/<team_id>', methods=['GET'])
def get_matches_for_home_team(team_id):
    try:
        matches = db.session.query(Match).filter(Match.home_team_id == team_id).order_by(Match.date)
        return json.dumps([row.to_dict() for row in matches])
    except Exception:
        return jsonify({'status': 'fail','message': 'Operation failed'}), 404


@matches_blueprint.route('/matches/home-team/<team_id>/upcoming', methods=['GET'])
def get_upcoming_matches_for_home_team(team_id):
    matches = Match.query.filter_by(home_team_id=team_id, goals_home_team=None)
    return json.dumps([row.to_dict() for row in matches])


@matches_blueprint.route('/matches/<match_id>', methods=['GET'])
def get_specific_match(match_id):
    result = Match.query.filter_by(id=match_id).first()
    return json.dumps(result.to_dict()), 200

@matches_blueprint.route('/matches/team/<team_id>', methods=['GET'])
def get_matches_from_team(team_id):
    result = db.session.query(Match).filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id)).order_by(Match.date)
    return json.dumps([row.to_dict() for row in result])

@matches_blueprint.route('/matches/division/<division_id>/matchweek/<matchweek_nr>', methods=['GET'])
def get_matches_in_division_from_matchweek(division_id, matchweek_nr):
    result = Match.query.filter_by(division_id=division_id, matchweek=matchweek_nr)
    return json.dumps([row.to_dict() for row in result]), 200


@matches_blueprint.route('/matches/matchweek/max', methods=['GET'])
def get_max_matchweeks():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    return jsonify({'max': maximum}), 200


@matches_blueprint.route('/matches/per-week', methods=['GET'])
def get_matches_per_week():
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    matches_per_week = dict()
    for i in range(1, maximum):
        matches_per_week[i] = [row.to_dict() for row in Match.query.filter_by(matchweek=i).order_by(Match.time)]
    return jsonify(matches_per_week)


@matches_blueprint.route('/matches/division/<division_id>/per-week', methods=['GET'])
def get_matches_per_week_for_division(division_id):
    maximum = db.session.query(func.max(Match.matchweek)).scalar()
    matches_per_week = dict()
    for i in range(1, maximum):
        matches_per_week[i] = [row.to_dict() for row in Match.query.filter_by(division_id=division_id, matchweek=i).order_by(Match.time)]
    return jsonify(matches_per_week)


@matches_blueprint.route('/matches/matchweek/<matchweek_nr>/referees/assigned')
def get_already_assigned_referees(matchweek_nr):
    matches = db.session.query(Match).filter(and_(Match.matchweek == matchweek_nr, Match.referee_id != None))
    return jsonify({'referee_ids' : [match.referee_id for match in matches]})


@matches_blueprint.route('/matches/division/<division_id>/best-attack', methods=['GET'])
def get_team_with_best_attack(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict = dict()
    for row in matches:
        score_dict.setdefault(row.home_team_id, 0)
        score_dict.setdefault(row.away_team_id, 0)
        if row.goals_home_team is not None:
            score_dict[row.home_team_id] += row.goals_home_team
            score_dict[row.away_team_id] += row.goals_away_team

    max_key = max(score_dict, key=score_dict.get)
    return json.dumps({'team': str(max_key), 'goals': score_dict[max_key]})


@matches_blueprint.route('/matches/division/<division_id>/best-defense', methods=['GET'])
def get_team_with_best_defense(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict = dict()
    for row in matches:
        if row.goals_away_team is not None:
            score_dict.setdefault(row.home_team_id, 0)
            score_dict.setdefault(row.away_team_id, 0)
            score_dict[row.home_team_id] += row.goals_away_team
            score_dict[row.away_team_id] += row.goals_home_team

    min_key = min(score_dict, key=score_dict.get)
    return json.dumps({'team': str(min_key), 'goals': score_dict[min_key]})


@matches_blueprint.route('/matches/division/<division_id>/most-clean-sheets', methods=['GET'])
def get_team_with_most_clean_sheets(division_id):
    matches = Match.query.filter_by(division_id=division_id)
    score_dict = dict()
    for row in matches:
        if row.goals_home_team == 0:
            score_dict.setdefault(row.away_team_id, 0)
            score_dict[row.away_team_id] += 1
        if row.goals_away_team == 0:
            score_dict.setdefault(row.home_team_id, 0)
            score_dict[row.home_team_id] += 1

    max_key = max(score_dict, key=score_dict.get)
    return json.dumps({'team': str(max_key), 'nr_of_clean_sheets': score_dict[max_key]})


@matches_blueprint.route('/matches/division/<division_id>/team-points', methods=['GET'])
def get_points_for_teams_in_division(division_id):
    team_rankings = dict()
    matches = Match.query.filter_by(division_id=division_id)
    for match in matches:
        team_id = match.home_team_id
        team_rankings.setdefault(team_id, 0)
        if match.goals_home_team is not None:
            if match.goals_home_team > match.goals_away_team:
                team_rankings[team_id] += 3  # home team wins
            elif match.goals_home_team == match.goals_away_team:
                team_rankings[team_id] += 1  # equal
    return jsonify(team_rankings)

@matches_blueprint.route('/matches/track-record/<team_id>', methods=['GET'])
def get_team_track_record(team_id):
    matches = db.session.query(Match).filter(and_(
        or_(Match.home_team_id == team_id, Match.away_team_id == team_id)),
        Match.goals_home_team != None)
    track_record = ""
    for match in sort_matches(matches)[-5:]:
        if match["goals_home_team"] > match["goals_away_team"]:
            if match["home_team_id"] == int(team_id):
                track_record += 'W'
            elif match["away_team_id"] == int(team_id):
                track_record += 'L'
        elif match["goals_home_team"] < match["goals_away_team"]:
            if match["home_team_id"] == int(team_id):
                track_record += 'L'
            elif match["away_team_id"] == int(team_id):
                track_record += 'W'
        else:
            track_record += 'D'
    return track_record


@matches_blueprint.route('/matches/statistics/<team_1_id>/vs/<team_2_id>', methods=['GET'])
def get_head_to_head_statistics(team_1_id, team_2_id):
    matches = db.session.query(Match).filter(and_(or_(
        and_(Match.home_team_id == team_1_id, Match.away_team_id == team_2_id), and_(
            Match.home_team_id == team_2_id, Match.away_team_id == team_1_id))),
            Match.goals_home_team != None)
    stats = {'count': 0, 'wins_1': 0, 'wins_2': 0, 'equal': 0}

    for match in matches:
        stats['count'] += 1
        if match.goals_home_team > match.goals_away_team:
            if match.home_team_id == team_1_id:
                stats['wins_1'] += 1
            else:
                stats['wins_2'] += 1
        elif match.goals_home_team < match.goals_away_team:
            if match.home_team_id == team_1_id:
                stats['wins_2'] += 1
            else:
                stats['wins_1'] += 1
        else:
            stats['equal'] += 1
    return json.dumps(stats)

@matches_blueprint.route('/matches/<team_1_id>/vs/<team_2_id>', methods=['GET'])
def get_recent_matches_two_teams(team_1_id, team_2_id):
    matches = db.session.query(Match).filter(and_(or_(
        and_(Match.home_team_id == team_1_id, Match.away_team_id == team_2_id), and_(
            Match.home_team_id == team_2_id, Match.away_team_id == team_1_id))),
            Match.goals_home_team != None)
    return json.dumps(sort_matches(matches)[-3:])

@matches_blueprint.route('/matches/division/<division_id>/statistics', methods=['GET'])
def get_division_statistics(division_id):
    div_stats = dict()
    matches = Match.query.filter_by(division_id=division_id)
    for match in matches:
        div_stats.setdefault(match.home_team_id,
                             {'played': 0, 'wun': 0, 'lost': 0, 'equal': 0, 'goals_for': 0, 'goals_against': 0})
        div_stats.setdefault(match.away_team_id,
                             {'played': 0, 'wun': 0, 'lost': 0, 'equal': 0, 'goals_for': 0, 'goals_against': 0})
        # update stats
        if match.goals_home_team is not None:
            div_stats[match.home_team_id]['played'] += 1
            div_stats[match.away_team_id]['played'] += 1
        else:
            continue  # match is not played yet
        if match.goals_home_team > match.goals_away_team:
            div_stats[match.home_team_id]['wun'] += 1
            div_stats[match.away_team_id]['lost'] += 1
        elif match.goals_home_team < match.goals_away_team:
            div_stats[match.home_team_id]['lost'] += 1
            div_stats[match.away_team_id]['wun'] += 1
        else:
            div_stats[match.home_team_id]['equal'] += 1
            div_stats[match.away_team_id]['equal'] += 1
        div_stats[match.home_team_id]['goals_for'] += match.goals_home_team
        div_stats[match.away_team_id]['goals_for'] += match.goals_away_team
        div_stats[match.home_team_id]['goals_against'] += match.goals_away_team
        div_stats[match.away_team_id]['goals_against'] += match.goals_home_team
    return jsonify(div_stats)

### OTHER REQUESTS ###
@matches_blueprint.route('/matches/<match_id>/score', methods=['PUT'])
def update_match_score(match_id):
    match = Match.query.filter_by(id=match_id).first()
    data = request.get_json()
    match.goals_home_team = int(data.get("home_score"))
    match.goals_away_team = int(data.get("away_score"))
    db.session.commit()
    return jsonify({'status' : 'succes'}), 200

@matches_blueprint.route('/matches/<match_id>/referee', methods=['POST'])
def update_referee(match_id):
    match = Match.query.filter_by(id=match_id).first()
    data = request.get_json()
    match.referee_id = int(data.get("new_id")) if data.get("new_id") != "None" else None
    db.session.commit()
    return jsonify({'status' : 'succes'}), 200
