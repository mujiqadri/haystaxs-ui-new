from flask import Blueprint, request, render_template, redirect, url_for, flash, g, session
from flask_login import login_user, login_required, logout_user, current_user
from webapp import db
from .db_models import User
from .data_services import cluster_data as cds, haystaxs as hds

_ppbp = Blueprint('pp', __name__)  # public portal


@_ppbp.before_request
def before_request():
    g.user_clusters = hds.get_clusters_of_user(current_user.get_id())


@_ppbp.route('/', endpoint='index')  # url_for can pick up the desired route using endpoint parameter or route
@_ppbp.route('/dashboard')
@login_required
def dashboard():
    return render_template('pp/dashboard.html', pg_title='Dashboard',
                           user_clusters=g.user_clusters, db_names=cds.get_db_names(),
                           user_names=cds.get_user_names())


@_ppbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = db.session.query(User).filter(User.email_address == request.form['login_email']).one()
        except Exception as ex:
            flash(ex)
            return render_template('pp/login.html')

        login_user(user)
        session['active_cluster_id'] = hds.get_default_cluster_id(current_user.get_id())
        return redirect(url_for('pp.dashboard'))
    else:
        return render_template('pp/login.html')


@_ppbp.route('/change-active-cluster')
def change_active_cluster():
    cluster_id = request.args['cluster_id']
    session['active_cluster_id'] = cluster_id
    return 'active cluster changed to {0}'.format(cluster_id)


@_ppbp.route('/logout')
@login_required
def logout():
    print(current_user.email_address)
    logout_user()
    return render_template('pp/login.html')
