from cerberus import Validator

schemaCompute = {
    'input': {'type': 'dict',
              'required': True,
              'schema': {
                  'description': {'type': 'string', 'required': True},
                  'goals': {'type': 'string', 'required': True}
              }
    },
    'data': {'type': 'string'},
    'filter': {'type': 'dict', 'allow_unknown': True,
               'schema': {
                   'uni': {'type': 'list'},
                   'semester': {'type': 'list'}
               }},
    'output': {'type': 'dict',
               'schema': {
                   'format': {'type': 'string', 'allowed': ['xml', 'json', 'csv']}
               }
    }
    # 'courseDescription': {'type': 'string', 'required': True},
    # 'courseGoals': {'type': 'string', 'required': True},
    # 'filterUni': {'type': 'list', 'required': False, 'schema': {'type': 'string'}},
    # 'filterSemester': {'type': 'list', 'required': False, 'schema': {'type': 'string', 'allowed': ['summer', 'winter']}},
    # 'outputFormat': {'type': 'string', 'allowed': ['json', 'xml', 'csv']},
}

validatorCompute = Validator(schemaCompute)
