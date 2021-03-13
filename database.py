import sqlite3
from flask import g

DATABASE_PATH = './courses.db'

LOGICAL_DISJUNCTION_JOIN = " OR "
LOGICAL_CONJUNCTION_JOIN = " AND "
COMMA_JOIN = ", "


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)

    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def generate_sql_filter(filter):
    sql_filters = []

    if "uni" in filter:
        unis = filter['uni']
        uni_like = [f'UNI LIKE "%{uni}%"' for uni in unis]
        uni_filter = f'({LOGICAL_DISJUNCTION_JOIN.join(uni_like)})'

        sql_filters.append(uni_filter)

    if "semester" in filter:
        semesters = filter['semester']
        semester_names = [f'"{semester}"' for semester in semesters]
        semester_filter = f'(SEMESTER in ({COMMA_JOIN.join(semester_names)}))'

        sql_filters.append(semester_filter)

    return f'WHERE {LOGICAL_CONJUNCTION_JOIN.join(sql_filters)}'
