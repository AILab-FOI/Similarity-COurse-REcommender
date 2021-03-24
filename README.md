# Similarity-COurse-REcommender

## How to Run it

```
usage: api.py [-h] [-d] [--host [HOST]] [--port [PORT]]

optional arguments:
  -h, --help     show this help message and exit
  -d             Debug mode
  --host [HOST]  Specify host for server to run on. DEFAULT: 0.0.0.0
  --port [PORT]  Specify port for server to run on. DEFAULT: 50021
```

## API Request Template

In order to provide a valid API request to the `[host]:[port]/score/compute` gateway, the JSON or GET arguments must conform to the following template:

```python
{
    'input': {'type': 'dict',
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
}
```

Example JSON request:

```json
'{"input":{"description":"jedanjakodobarpredmet","goals":"learnhowtolearn"},"output":{"format":"json"},"filter":{"semester":["winter"]}}'
```

Example GET request:

```
http://[host]:[port]/score/compute?input={%22description%22:%22jedanjakodobarpredmet%22,%22goals%22:%22learnhowtolearn%22}&output={%22format%22:%22json%22}&filter={%22semester%22:[%22summer%22],%22uni%22:[%22Zil%22]}
```
