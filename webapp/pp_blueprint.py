from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from webapp import db
from .db_models import User

publicportal_bp = Blueprint('pp', __name__)

_ppbp = publicportal_bp

@_ppbp.route('/', endpoint='index') # url_for can pick up the desired route using endpoint parameter or route
@_ppbp.route('/dashboard')
@login_required
def dashboard():
    return render_template('pp/dashboard.html')

@_ppbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = db.session.query(User).filter(User.email_address == request.form['login_email']).one()
        except Exception as ex:
            flash(ex)
            return render_template('pp/login.html')

        login_user(user)
        return redirect(url_for('pp.dashboard'))
    else:
        return render_template('pp/login.html')

@_ppbp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('pp/login.html')
