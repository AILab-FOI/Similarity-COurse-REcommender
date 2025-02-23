import sqlite3
from flask import g

DATABASE_PATH = './courses.db'

LOGICAL_DISJUNCTION_JOIN = " OR "
LOGICAL_CONJUNCTION_JOIN = " AND "
COMMA_JOIN = ", "


def connect_to_db():
    return sqlite3.connect(DATABASE_PATH)


def close_db_connection(db_connection=None):
    if db_connection is None:
        db_connection = getattr(g, '_database', None)

    if db_connection is not None:
        db_connection.close()


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = connect_to_db()

    return db


def query_db(query, db_connection=None, args=(), one=False):
    """Fetch data from a DB.
    If no connection is given, then connect to a DB.
    Close connection when finished.

    Parameters
    ----------
    query : type
        The SQL query to be executed.
    db_connection : type
        DB connection instance.
    args : type
        Additional arguments to be forwarded to sqlite3.execute()
    one : type
        True if only 1 row is to be returned.

    Returns
    -------
    Returns a list of dictionaries. Each item is a row of fetched data.
    Dictionary keys are column names of the fetched data.

    """
    if db_connection is None:
        db_connection = connect_to_db()

    db_connection.row_factory = sqlite3.Row

    cur = db_connection.cursor()

    cur.execute(query, args)
    rv = [dict(row) for row in cur.fetchall()]
    cur.close()

    close_db_connection(db_connection)

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
