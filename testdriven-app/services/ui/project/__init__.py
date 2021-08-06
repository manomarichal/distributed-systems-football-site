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
    from project.api.misc import ui_misc_blueprint
    from project.api.divisions import ui_divisions_blueprint
    from project.api.teams import ui_teams_blueprint
    from project.api.matches import ui_matches_blueprint
    app.register_blueprint(ui_login_blueprint)
    app.register_blueprint(ui_misc_blueprint)
    app.register_blueprint(ui_divisions_blueprint)
    app.register_blueprint(ui_teams_blueprint)
    app.register_blueprint(ui_matches_blueprint)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app

