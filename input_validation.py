from cerberus import Validator

input_schema = {
    'type': 'dict', 'schema': {
        'description': {"type": 'string', "required": True},
        'goals': {"type": 'string', "required": True}
    }
}

filter_schema = {
    'type': 'dict', 'schema': {
        'univ': {'type': 'list', "required": False, 'items': [{'type': 'string'}]},
        'semester': {'type': 'list', "required": False, 'items': [{'type': 'string', 'allowed': ['summer', 'winter']}]}
    }
}

output_format_schema = {
    'type': 'string',
    'allowed': ['json', 'xml', 'csv']
}

schema = {
    'input': input_schema,
    'filter': filter_schema,
    'outputFormat': output_format_schema,
}

validator = Validator(schema)
