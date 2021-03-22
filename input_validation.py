from cerberus import Validator

schema = {
    'courseDescription': {"type": 'string', "required": True},
    'courseGoals': {"type": 'string', "required": True},
    'filterUni': {'type': 'list', "required": False, 'schema': {'type': 'string'}},
    'filterSemester': {'type': 'list', "required": False, 'schema': {'type': 'string', 'allowed': ['summer', 'winter']}},
    'outputFormat': {'type': 'string', 'allowed': ['json', 'xml', 'csv']},
}

validator = Validator(schema)
