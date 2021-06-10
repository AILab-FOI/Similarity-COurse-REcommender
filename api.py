from flask import Flask, request
import input_validation as validator
from database import query_db, generate_sql_filter, close_db_connection
from data_processing import generate_response
from similarity import compute_similarity, configure_LSA
import json
import argparse

app = Flask(__name__)

lsi_model = None
lsa_index = None


def get_all_data(filters=''):
    if filters:
        filters = generate_sql_filter(filters)

    query = f'SELECT * FROM COURSE {filters}'
    return query_db(query)


def configure_similarity_alg():
    global lsi_model
    global lsa_index

    # fetch courses from db
    courses = get_all_data()

    # generate lsi model & index
    lsi_model, lsa_index = configure_LSA(courses)


def extract_contents(request, endpoint: str):
    try:
        if request.is_json:
            content = request.json
        elif request.method in ['POST', 'GET']:
            content = {k: json.loads(v) for k, v in request.values.items()}
        else:
            return {'error': 'API request error. Bad request formatting.'}
    except Exception as e:
        print(e)
        return {'error': 'API request error. Bad request formatting.'}

    # validate input
    if endpoint == 'compute':
        if not validator.validatorCompute.validate(content):
            return {"error": validator.validatorCompute.errors}
    elif endpoint == 'fetchdata':
        if not validator.validatorFetchData.validate(content):
            return {"error": validator.validatorFetchData.errors}

    return content


@app.route('/score/fetchdata', methods=['GET', 'POST'])
def fetch_data():
    content = extract_contents(request, 'fetchdata')

    # generate SQL filter query
    courses = get_all_data(filters=content.get('filter', ''))

    # generate response based on desired fomrat
    output = generate_response(
        content.get('output', {'format': 'json'}).get('format'), courses)

    return output


@app.route('/score/compute', methods=['GET', 'POST'])
def check_courses_similarity():
    content = extract_contents(request, 'compute')

    # generate SQL filter query
    courses = get_all_data(filters=content.get('filter', ''))

    # calculate similarity
    courses_json_similarities = compute_similarity(
        content['input'], courses, lsi_model, lsa_index)

    # generate response based on desired fomrat
    output = generate_response(
        content.get('output', {'format': 'json'}).get('format'),
        courses_json_similarities[:3])

    return output


@ app.teardown_appcontext
def close_connection(exception):
    try:
        close_db_connection()
    except Exception:
        pass


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
