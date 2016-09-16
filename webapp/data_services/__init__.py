from webapp import db
from webapp.config import active_config

def get_connection_hs_schema():
    conn = db.engine.connect()
    conn.execute("SET search_path = {schema}".format(schema=active_config.HAYSTACK_SCHEMA))
    return conn

def get_connection_cluster_data_schema():
    conn = db.engine.connect()
    conn.execute("SET search_path = {schema}".format(schema=active_config.CLUSTER_DATA_SCHEMA))
    return conn
