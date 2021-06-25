from flask import Blueprint, jsonify, render_template, request
import requests

ui_login_blueprint = Blueprint('login', __name__, template_folder='./templates')

@ui_login_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@ui_login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    response = requests.get('http://localhost:5002/users/ping')
    return response
    if request.method == 'POST':
        return render_template("test.html")
    return render_template("login.html")