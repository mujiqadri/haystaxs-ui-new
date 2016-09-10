from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from .config import active_config

######################
### Create the App ###
######################
theapp = Flask(__name__)
theapp.config.from_object(active_config)

sa_metadata = MetaData(schema=active_config.HAYSTACK_SCHEMA)
db = SQLAlchemy(theapp, metadata=sa_metadata)

###############################
### Init Session Managment  ###
###############################
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(theapp)

from . import pp_blueprint

###############################
### Register Blueprints     ###
###############################
theapp.register_blueprint(pp_blueprint.publicportal_bp)

login_manager.login_view = 'pp.login'

from .db_models import User

# Initialize the User Loader
@login_manager.user_loader
def load_user(user_id):
    # TODO: How to make this not access the DB on each call
    user = db.session.query(User).filter(User.user_id == user_id).one()
    return user

print('Flask App initialize successful')

# import logging
# theapp.logger.addHandler(logging.StreamHandler())
# theapp.logger.critical('Abay chiknay CRITICAL')
# for logger_name in logging.Logger.manager.loggerDict.keys():
#     print(logger_name)

# from . import db_models