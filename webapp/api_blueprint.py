from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user
from webapp import db
from .db_models import User

_apibp = Blueprint('api', __name__, url_prefix='/api')


@_apibp.route('/dashboard/chartdata/durationandcounts')
def dashboard_duration_and_counts_chart_data():
    return jsonify([{"date": "2016-02-04", "queryType": "INSERT SELECT", "count": 233, "duration": 1463.0},
                    {"date": "2016-02-04", "queryType": "SELECT", "count": 408, "duration": 2.0},
                    {"date": "2016-02-05", "queryType": "INSERT SELECT", "count": 35, "duration": 6830.0},
                    {"date": "2016-02-05", "queryType": "SELECT", "count": 72, "duration": 83.0},
                    {"date": "2016-02-10", "queryType": "UNRESOLVED", "count": 1, "duration": 2.0},
                    {"date": "2016-03-08", "queryType": "SELECT", "count": 14, "duration": 6.0},
                    {"date": "2016-03-11", "queryType": "INSERT SELECT", "count": 65, "duration": 297.0},
                    {"date": "2016-03-11", "queryType": "MULTIPLE SQL STATEMENTS", "count": 4, "duration": 1.0},
                    {"date": "2016-03-11", "queryType": "SELECT", "count": 155, "duration": 522.0},
                    {"date": "2016-04-02", "queryType": "SELECT", "count": 34, "duration": 473.0},
                    {"date": "2016-07-04", "queryType": "SELECT", "count": 23, "duration": 2.0},
                    {"date": "2016-07-05", "queryType": "SELECT", "count": 60, "duration": 3.0},
                    {"date": "2016-07-18", "queryType": "SELECT", "count": 462, "duration": 1.0}])


@_apibp.route('/dashboard/chartdata/hourlydata')
def dashboard_hourly_chart_data():
    return jsonify(
        [{"queryType": "INSERT SELECT", "hour": 8, "duration": 151.0}, {"queryType": "INSERT SELECT", "hour": 9, "duration": 20.0},
         {"queryType": "SELECT", "hour": 9, "duration": 4.0}, {"queryType": "INSERT SELECT", "hour": 10, "duration": 88.0},
         {"queryType": "SELECT", "hour": 10, "duration": 6.0}, {"queryType": "INSERT SELECT", "hour": 11, "duration": 1687.0},
         {"queryType": "SELECT", "hour": 11, "duration": 118.0}, {"queryType": "INSERT SELECT", "hour": 12, "duration": 41.0},
         {"queryType": "SELECT", "hour": 12, "duration": 7.0}, {"queryType": "INSERT SELECT", "hour": 15, "duration": 87.0},
         {"queryType": "INSERT SELECT", "hour": 18, "duration": 136.0}, {"queryType": "SELECT", "hour": 21, "duration": 1.0},
         {"queryType": "INSERT SELECT", "hour": 23, "duration": 102.0}, {"queryType": "UNRESOLVED", "hour": 23, "duration": 2.0}])
