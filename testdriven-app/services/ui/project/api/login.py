from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from project.api.models import User
from project.api.forms import LoginForm

ui_login_blueprint = Blueprint('login', __name__, template_folder='./templates')

@ui_login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('misc.show_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return redirect(url_for('login.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('misc.show_home'))
    else:
        pass
        return render_template('login.html', title='Sign In', form=form)

@ui_login_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))
