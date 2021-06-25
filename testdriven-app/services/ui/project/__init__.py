from flask import Flask, jsonify
from flask_login import LoginManager

import os


def create_app(script_info=None):
    app = Flask(__name__)
    login = LoginManager
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.login import ui_login_blueprint
    app.register_blueprint(ui_login_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app

