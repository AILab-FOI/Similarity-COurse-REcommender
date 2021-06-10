from cerberus import Validator

schemaCompute = {
    'input': {'type': 'dict',
              'required': True,
              'schema': {
                  'description': {'type': 'string', 'required': True},
                  'goals': {'type': 'string', 'required': True}
              }},
    'data': {'type': 'dict',
             'schema': {
                 'source': {'type': 'string'}
             }},
    'filter': {'type': 'dict', 'allow_unknown': True,
               'schema': {
                   'uni': {'type': 'list'},
                   'semester': {'type': 'list'}
               }},
    'output': {'type': 'dict',
               'schema': {
                   'format': {'type': 'string', 'allowed':
                              ['xml', 'json', 'csv']}
               }}
}

validatorCompute = Validator(schemaCompute)

schemaFetchData = {
    'output': {'type': 'dict',
               'schema': {
                   'format': {'type': 'string', 'allowed':
                              ['xml', 'json', 'csv']}
               }}
}

validatorFetchData = Validator(schemaFetchData)
