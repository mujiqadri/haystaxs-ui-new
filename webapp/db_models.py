import re
import inflect
from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from webapp import db

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

# db.engine.echo = False
db.metadata.bind = db.engine

am_base = automap_base(metadata=db.metadata)

class User(am_base, UserMixin):
    __tablename__ = 'users'

    def get_id(self):
        return str(self.user_id)

am_base.prepare(db.engine,
                reflect=True,
                classname_for_table=camelize_and_singularize_classname,
                name_for_collection_relationship=pluralize_collection)

# REMEMBER: User is now == am_base.classes.User, I don't fucking know how but it is, it's like fucking magic !
# user_2 = db.session.query(User).filter(User.user_id == 1).one()

print('Haystaxs Models creation successful.')
