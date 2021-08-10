from flask import Flask, jsonify, render_template, url_for
from flask_login import LoginManager, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# instantiate db
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(script_info=None):
    app = Flask(__name__)

    # login
    login_manager.init_app(app)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    # register blueprints
    from project.api.login import ui_login_blueprint
    from project.api.misc import ui_misc_blueprint
    from project.api.divisions import ui_divisions_blueprint
    from project.api.teams import ui_teams_blueprint
    from project.api.matches import ui_matches_blueprint
    from project.api.users import ui_users_blueprint
    app.register_blueprint(ui_login_blueprint)
    app.register_blueprint(ui_users_blueprint)
    app.register_blueprint(ui_misc_blueprint)
    app.register_blueprint(ui_divisions_blueprint)
    app.register_blueprint(ui_teams_blueprint)
    app.register_blueprint(ui_matches_blueprint)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    # admin interface
    admin = Admin(app, template_mode='bootstrap4')

    class SecureView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.admin:
                    return True
                else:
                    return False
    try:
        # leagues database connection
        leagues_engine = create_engine("postgresql://postgres:postgres@leagues-db:5432/leagues_dev")
        leagues_session = sessionmaker(leagues_engine)
        leagues_session = leagues_session()

        leagues_metadata = MetaData(bind=leagues_engine, reflect=True)
        LeaguesBase = declarative_base()

        class Match(LeaguesBase):
            __table__ = Table('matches', leagues_metadata, autoload_with=leagues_engine)
        class Division(LeaguesBase):
            __table__ = Table('divisions', leagues_metadata, autoload_with=leagues_engine)

        admin.add_view(SecureView(Match, leagues_session))
        admin.add_view(SecureView(Division, leagues_session))
    except Exception:
        pass

    try:
        # teams database connection
        teams_engine = create_engine("postgresql://postgres:postgres@teams-db:5432/teams_dev")
        teams_session = sessionmaker(teams_engine)
        teams_session = teams_session()

        teams_metadata = MetaData(bind=teams_engine, reflect=True)
        TeamsBase = declarative_base()

        class Team(TeamsBase):
            __table__ = Table('teams', teams_metadata, autoload_with=teams_engine)
            can_create = True
        class Club(TeamsBase):
            __table__ = Table('clubs', teams_metadata, autoload_with=teams_engine)
            can_create = True

        admin.add_view(SecureView(Team, teams_session))
        admin.add_view(SecureView(Club, teams_session))
    except Exception:
        pass

    try:
        # teams database connection
        users_engine = create_engine("postgresql://postgres:postgres@users-db:5432/users_dev")
        users_session = sessionmaker(users_engine)
        users_session = users_session()

        users_metadata = MetaData(bind=users_engine, reflect=True)
        UsersBase = declarative_base()

        class User(UsersBase):
            __table__ = Table('users', users_metadata, autoload_with=teams_engine)
            can_create = True

        admin.add_view(SecureView(User, users_session))
    except Exception:
        pass

    @app.before_first_request
    def restrict_admin_url():
        endpoint = 'admin.index'
        url = url_for(endpoint)
        admin_index = app.view_functions.pop(endpoint)

        @app.route(url, endpoint=endpoint)
        @login_required
        def secure_admin_index():
            if current_user.admin:
                return admin_index()
            return render_template("not_authorized.html")

    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app

