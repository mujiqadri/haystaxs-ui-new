from flask import Blueprint, jsonify, session, render_template,g,request
from webapp.data_services import haystaxs as hds
from webapp.data_services import cluster_data as cd
from flask_login import login_user, login_required, logout_user, current_user

_apibp = Blueprint('api', __name__, url_prefix='/api')

@_apibp.before_request
def before_request():
    g.user_clusters = hds.get_clusters_of_user(current_user.get_id())

@_apibp.route('/dashboard/chartdata/durationandcounts')
def dashboard_duration_and_counts_chart_data():
    user_name = request.args['userName']
    db_name = request.args['dbName']
    from_date = ""
    to_date = "";
    active_cluster_id = session['active_cluster_id']
    query_duration_and_count = cd.get_query_stats_for_charts(active_cluster_id,from_date,to_date,db_name,user_name)
    return jsonify(query_duration_and_count)

@_apibp.route('/dashboard/chartdata/hourlydata')
def dashboard_hourly_chart_data():
    from_date = ""
    to_date = "";
    db_name = ""
    username = "";
    active_cluster_id = session['active_cluster_id']
    windowOp = 'avg'
    hourly_chart_data = cd.get_hourly_query_stats_for_charts(active_cluster_id, from_date, to_date, db_name, username, windowOp)
    return jsonify(hourly_chart_data)

@_apibp.route('/workload-json/<workload_id>')
def workload_json(workload_id):
    return hds.get_workload_json(workload_id)

@_apibp.route('/workloads_list')
def workloads_list():
    if 'active_cluster_id' in session:
        active_cluster_id = session['active_cluster_id']
        workloads = hds.get_lastn_workloads(active_cluster_id)
    return render_template('pp/work_load_list.html', workloads = workloads)
