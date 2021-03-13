
import pandas as pd
import json
from flask import Response
from json2xml import json2xml

CSV_FILE_NAME = "courses.csv"


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


def generate_csv_response(courses_json):
    data = json.loads(json.dumps(courses_json))
    df = pd.json_normalize(data)
    csv = df.to_csv(index=False)

    response = Response(csv)
    response.headers["Content-Disposition"] = f"attachment; filename={CSV_FILE_NAME}"
    response.headers["Content-type"] = "text/csv"

    return response


def generate_xml_response(courses_json):
    json_response = generate_json_response(courses_json)
    xml = json2xml.Json2xml(json_response).to_xml()

    response = Response(xml, mimetype='text/xml')

    return response


def generate_json_response(courses_json):
    return {"courses": courses_json}


def generate_response(format, courses_json):
    if format == 'csv':
        return generate_csv_response(courses_json)

    if format == 'xml':
        return generate_xml_response(courses_json)

    return generate_json_response(courses_json)
