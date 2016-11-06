from . import get_connection_cluster_data_schema
from . import active_config
import datetime

def get_query_stats_for_charts(cluster_id, from_date, to_date, db_name, user_name):
    with get_connection_cluster_data_schema() as conn:
        where_clause = " WHERE cluster_id = '{0}' ".format(cluster_id)

        if (from_date and to_date):
            where_clause += " AND logsessiontime::date >= '{0}'".format(from_date)
            where_clause += " AND logsessiontime::date <= '{0}'".format(to_date)
            prepend_and = True
        if (db_name):
            where_clause += " AND logdatabase = '{0}'".format(db_name)
        if (user_name):
            where_clause += " AND loguser = '{0}'".format(user_name)

        sql = """select * from(select logsessiontime::date date, qryType query_type, count(0) count,
                round(coalesce(sum(extract(epoch from logduration)),0)) as duration
                from {user_schema}.queries
                {where_clause}
                group by logsessiontime::date, qrytype
                ORDER BY logsessiontime::date) as Y where duration > 0
                """.format(user_schema=active_config.USER_SCHEMA, where_clause=where_clause);

        cursor = conn.execute(sql)
        result = cursor.fetchall();
        duration_and_counts = []
        for row in result:
            query_data = {
                "date": row[0].strftime("%Y-%m-%d"),
                "queryType": row[1],
                "count": row[2],
                "duration": row[3]}

            duration_and_counts.append(query_data)
            return duration_and_counts

def get_hourly_query_stats_for_charts(cluster_id, from_date, to_date, db_name, user_name, windowOp):
    with get_connection_cluster_data_schema() as conn:
        where_clause = " WHERE cluster_id = '{0}' ".format(cluster_id)

        if (from_date and to_date):
            where_clause += " AND logsessiontime::date >= '{0}'".format(from_date)
            where_clause += " AND logsessiontime::date <= '{0}'".format(to_date)
            prepend_and = True
        if (db_name):
            where_clause += " AND logdatabase = '{0}'".format(db_name)
        if (user_name):
            where_clause += " AND loguser = '{0}'".format(user_name)


        sql = """select * from(select qrytype query_type, extract(hour from logsessiontime) as hour, round({windowOp}(extract(epoch from logduration)))
                 as duration from {user_schema}.queries {where_clause} and
                 extract(epoch from logduration) > 0
                group by EXTRACT(hour from logsessiontime),
                 qrytype ORDER BY EXTRACT(hour from logsessiontime), qrytype
                 ) as Y where duration > 0;""".format(user_schema=active_config.USER_SCHEMA, where_clause=where_clause,windowOp = windowOp)
        cursor = conn.execute(sql)
        result = cursor.fetchall();

        hourly_chart_data = []
        for row in result:
            query_data = {
                "queryType": row[0],
                "hour": row[1],
                "duration": row[2]}

            hourly_chart_data.append(query_data)

        return hourly_chart_data

def get_db_names():
    with get_connection_cluster_data_schema() as conn:
        sql = "select value from query_metadata where type = '{0}' order by 1".format('dbname')
        result = [r[0] for r in conn.execute(sql)]

    return result

def get_user_names():
    with get_connection_cluster_data_schema() as conn:
        sql = "select value from query_metadata where type = '{0}' order by 1".format('username')
        result = [r[0] for r in conn.execute(sql)]

    return result