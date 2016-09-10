import os

# basedir = os.path.abspath(os.path.dirname(__file__))

class _ConfigBase:
    ###############################
    ### Custom Configs          ###
    ###############################
    # This config is used specifically by flask_sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://gpadmin:S3cr3t!@24.150.86.245:5432/haystack'
    HAYSTACK_SCHEMA = 'haystack_ui'
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
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:q90210@localhost:5432/haystack'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://gpadmin:S3cr3t!@24.150.86.245:5432/haystack'
    SQLALCHEMY_ECHO = True

class _ProdConfig(_ConfigBase):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gpadmin:S3cr3t!@192.168.1.240:5432/haystack'

_configs = {
    'Dev': _DevConfig(),
    'Prod': _ProdConfig()
}

_ENVAR_HAYSTAXS_CONFIG = 'HAYSTAXS_CONFIG'

active_config = _configs[os.getenv(_ENVAR_HAYSTAXS_CONFIG)]