from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

# instantiate db
db = SQLAlchemy()

def create_app(script_info=None):
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    # register blueprints
    from project.api.teams import teams_blueprint
    app.register_blueprint(teams_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app

