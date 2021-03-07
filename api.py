from flask import Flask, request, g
from input_validation import validator
from database import query_db


app = Flask(__name__)


@app.route('/check-similarity', methods=['POST'])
def hello():
    content = request.get_json()

    if not validator.validate(content):
        return {"status": "error", "error": validator.errors}

    courses = query_db('SELECT name FROM COURSE')
    print(courses)

    return {"success": True}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
