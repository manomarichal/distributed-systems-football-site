from flask import Blueprint, jsonify, render_template, request
import requests

ui_misc_blueprint = Blueprint('misc', __name__, template_folder='./templates')

@ui_misc_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success','message': 'pong!'})

@ui_misc_blueprint.route('/', methods=['GET'])
def show_home():
    return render_template("home.html")
