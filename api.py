from flask import Flask, request
from cerberus import Validator
from schema import schema

app = Flask(__name__)

v = Validator(schema)


@app.route('/check-similarity', methods=['POST'])
def hello():
    content = request.get_json()

    if not v.validate(content, schema):
        return {"status": "error", "error": v.errors}

    return {"success": True}


if __name__ == '__main__':
    app.run()
