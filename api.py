from flask import Flask, request, g
from input_validation import validatorCompute
from database import query_db, generate_sql_filter, connect_to_db, close_db_connection
from data_processing import course_row_to_json, generate_response
from similarity import compute_similarity, configure_LSA
import json
import argparse

app = Flask(__name__)

lsi_model = None
lsa_index = None


def configure_similarity_alg():
    global lsi_model
    global lsa_index

    # fetch courses from db
    db_connection = connect_to_db()
    courses = query_db(
        f'SELECT NAME, UNI, COURSE_ID, CREDITS, SEMESTER, DESCRIPTION, GOALS FROM COURSE', db_connection)

    # format courses data to json
    courses_json = [course_row_to_json(course) for course in courses]

    # generate lsi model & index
    lsi_model, lsa_index = configure_LSA(courses_json)

    close_db_connection(db_connection)


@app.route('/score/compute', methods=['GET', 'POST'])
def check_courses_similarity():
    if request.is_json:
        content = request.json
    elif request.method in ['POST', 'GET']:
        content = {k: json.loads(v) for k, v in request.values.items()}
    else:
        return {'error': 'API request error. Bad request formatting.'}

    # validate input
    if not validatorCompute.validate(content):
        return {"error": validatorCompute.errors}

    # return {'success': 'it works'}

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
        content['output']['format'], courses_json_similarities[:3])

    return output


@ app.teardown_appcontext
def close_connection(exception):
    close_db_connection()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="debugvar", action="store_true",
                        help="Debug mode")
    parser.add_argument("--host", const=True, nargs='?', type=str,
                        help="Specify host for server to run on. DEFAULT: 0.0.0.0")
    parser.add_argument("--port", const=True, nargs='?', type=int,
                        help="Specify port for server to run on. DEFAULT: 50021")
    parser.set_defaults(
        debugvar=False,
        host='0.0.0.0',
        port=50021
    )
    args = parser.parse_args()

    configure_similarity_alg()
    app.run(host=args.host, port=args.port, debug=args.debugvar)
