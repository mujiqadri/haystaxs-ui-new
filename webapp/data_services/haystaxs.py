from sqlalchemy import text, and_
from . import get_connection_hs_schema
from webapp import db
from webapp.db_models import Cluster, ClusterUser


def get_all_users(cluster_id):
    with get_connection_hs_schema() as conn:
        # Note: Need to figure out the purpose of text
        cursor = conn.execute(text("""
            select u.*, cu.* from users u, cluster_users cu
            where cu.cluster_id = :cluster_id
            and cu.user_id = u.user_id
        """), cluster_id=cluster_id)
        users = [u for u in cursor]

    return users


def get_clusters_of_user(user_id):
    query = db.session.query(Cluster.cluster_id, Cluster.friendly_name, ClusterUser.is_default). \
        filter(Cluster.cluster_id == ClusterUser.cluster_id). \
        filter(ClusterUser.user_id == user_id)
    # print(query)
    return query.all()


def get_default_cluster_id(user_id):
    query = db.session.query(ClusterUser.cluster_id). \
        filter(and_(ClusterUser.user_id == user_id, ClusterUser.is_default == True))
    return query.scalar()

def get_workload_json(workload_id):
    with get_connection_hs_schema() as conn:
        sql = "select workload_json from workloads_json where workload_id = {0}".format(workload_id)
        cursor = conn.execute(sql)
        result = cursor.fetchone()[0]

    return result


def get_lastn_workloads(gpsdId):
    with get_connection_hs_schema() as conn:
        sql = "select wl.* from workloads wl where wl.cluster_id = {0} order BY workload_id DESC".format(gpsdId)
        cursor = conn.execute(sql)
        workloads = [w for w in cursor]
    return workloads