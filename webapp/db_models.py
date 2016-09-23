import re
import inflect
from sqlalchemy import Column, Text
from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from webapp import db, active_config

########################################################################
### Helper for Automap to Generate ClassNames and Relationship names ###
########################################################################
_inflection_engine = inflect.engine()


def camelize_and_singularize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"

    singularized_tablename = _inflection_engine.singular_noun(tablename)
    if not singularized_tablename:
        singularized_tablename = tablename

    class_name = str(singularized_tablename[0].upper() + re.sub(r'_([a-z])', lambda m: m.group(1).upper(), singularized_tablename[1:]))
    return class_name


def pluralize_collection(base, local_cls, referred_cls, constraint):
    "Produce an 'uncamelized', 'pluralized' class name, e.g. "
    "'SomeTerm' -> 'some_terms'"

    referred_name = referred_cls.__name__
    # uncamelized = re.sub(r'[A-Z]', lambda m: "_%s" % m.group(0).lower(), referred_name)[1:]
    pluralized = _inflection_engine.plural(referred_name)
    return pluralized

######################################
### Configure Metadata and Automap ###
######################################
tables_to_reflect = ['users', 'cluster', 'cluster_users', 'workloads_json', 'workloads']

# db.engine.echo = False
db.metadata.bind = db.engine
db.metadata.reflect(only=tables_to_reflect)
am_base = automap_base(metadata=db.metadata)


###############################
### Haystaxs Schema Models  ###
###############################
class User(am_base, UserMixin):
    __tablename__ = 'users'

    def get_id(self):
        return str(self.user_id)


class Cluster(am_base):
    __tablename__ = 'cluster'


class ClusterUser(am_base):
    __tablename__ = 'cluster_users'

# class WlTable(am_base):
#     __tablename__ = 'wl_table'

###################################
### Cluster Data Schema Models  ###
###################################
class QueryMetadata(am_base):
    __tablename__ = 'query_metadata'
    __table_args__ = {'schema': active_config.CLUSTER_DATA_SCHEMA}

    type = Column(Text, primary_key=True)
    value = Column(Text, primary_key=True)

    # __mapper_args__ = {
    #     'extend_existing': True
    #     'primary_key': [QueryMetadata.__table__.c.type, query_metadata.c.value]
    # }


am_base.prepare(
    # db.engine,
    # reflect=True,
    classname_for_table=camelize_and_singularize_classname,
    name_for_collection_relationship=pluralize_collection)

###############################
### Just some testing code  ###
###############################
# REMEMBER: User is now == am_base.classes.User, I don't fucking know how but it is, it's like fucking magic !
# user_2 = db.session.query(User).filter(User.user_id == 1).one()

# This is happening when I'm reflecting all the tables, need to figure out where the collision is occuring...
# sqlalchemy.exc.ArgumentError: Error creating backref 'WlTableColumns' on relationship 'WlTableColumn.wltable':
#   property of that name exists on mapper 'Mapper|WlTable|wl_table'

# qmd = db.session.query(QueryMetadata).filter(QueryMetadata.type == 'dbname').all()
# for record in qmd:
#     print(record.value)

print('Db Models creation successful.')
