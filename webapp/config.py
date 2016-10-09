import configparser
import os

basedir = os.path.abspath(os.path.dirname(__file__))

ini = configparser.ConfigParser()
ini.read(os.path.join(basedir,  'config.ini'))


class _ConfigBase:
    ###############################
    ### Custom Configs          ###
    ###############################
    # This config is used specifically by flask_sqlalchemy
    SQLALCHEMY_DATABASE_URI = ''
    HAYSTACK_SCHEMA = 'haystack_ui'
    CLUSTER_DATA_SCHEMA = 'cluster_dot_admin_at_haystaxs_dot_com'
    USER_SCHEMA = 'cluster_dot_admin_at_haystaxs_dot_com'

    ###############################
    ### Flask Configs           ###
    ###############################
    HOST = None
    SECRET_KEY = "secret key for session usage"

class _DevConfig(_ConfigBase):
    # HOST = "0.0.0.0"
    PORT = 5001
    DEBUG = True
    #TEMPLATES_AUTO_RELOAD = True
    #EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_DATABASE_URI = ini['DEV']['DB URL']
    SQLALCHEMY_ECHO = False

class _ProdConfig(_ConfigBase):
    SQLALCHEMY_DATABASE_URI = ''

_configs = {
    'DEV': _DevConfig(),
    'PROD': _ProdConfig()
}

_ENVAR_HAYSTAXS_CONFIG = 'HAYSTAXS_CONFIG'

active_config = _configs[os.getenv(_ENVAR_HAYSTAXS_CONFIG)]