from flask import Flask, request, g
from input_validation import validator
from database import query_db, generate_sql_filter
from data_processing import course_row_to_json, generate_response
from similarity import compute_similarity, configure_LSA

app = Flask(__name__)

lsi_model = None
lsa_index = None


def configure_similarity_alg():
    global lsi_model, lsa_index

    # fetch courses from db
    courses = query_db(
        f'SELECT NAME, UNI, COURSE_ID, CREDITS, SEMESTER, DESCRIPTION, GOALS FROM COURSE')

    # format courses data to json
    courses_json = [course_row_to_json(course) for course in courses]

    # generate lsi model & index
    lsi_model, lsa_index = configure_LSA(courses_json)


@app.route('/check-courses-similarity', methods=['POST'])
def check_courses_similarity():
    content = request.get_json()

    # validate input
    if not validator.validate(content):
        return {"error": validator.errors}

    # generate SQL filter query
    sql_filter = ""
    if "filter" in content:
        sql_filter = generate_sql_filter(content['filter'])

    # fetch courses from db
    courses = query_db(
        f'SELECT NAME, UNI, COURSE_ID, CREDITS, SEMESTER, DESCRIPTION, GOALS FROM COURSE {sql_filter}')

    # format courses data to json
    courses_json = [course_row_to_json(course) for course in courses]

    # calculate similarity
    courses_json_similarities = compute_similarity(
        content['input'], courses_json, lsi_model, lsa_index)

    # generate response based on desired fomrat
    output = generate_response(
        content['outputFormat'], courses_json_similarities)

    return output


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    configure_similarity_alg()
    app.run()
