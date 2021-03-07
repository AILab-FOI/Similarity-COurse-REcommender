from flask import Flask, request, g
from input_validation import validator
from database import query_db


app = Flask(__name__)

LOGICAL_DISJUNCTION_JOIN = " OR "
LOGICAL_CONJUNCTION_JOIN = " AND "
COMMA_JOIN = ", "


def course_row_to_json(record):
    name, uni, courseId, credits, semester, description, goals = record

    return {
        'name': name,
        'uni': uni,
        'courseId': courseId,
        'credits': credits,
        'semester': semester,
        'description': description,
        'goals': goals,
    }


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


@app.route('/check-similarity', methods=['POST'])
def hello():
    content = request.get_json()

    if not validator.validate(content):
        return {"status": "error", "error": validator.errors}

    sql_filter = generate_sql_filter(content['filter'])

    courses = query_db(
        f'SELECT NAME, UNI, COURSE_ID, CREDITS, SEMESTER, DESCRIPTION, GOALS FROM COURSE {sql_filter}')
    courses_json = [course_row_to_json(course)
                    for course in courses]

    return {"success": True, "courses": courses_json}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
