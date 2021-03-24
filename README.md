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

```json
{
    "input": {"type": "dict",
              "required": true,
              "schema": {
                  "description": {"type": "string", "required": true},
                  "goals": {"type": "string", "required": true}
              }
    },
    "data": {"type": "string"},
    "filter": {"type": "dict", "allow_unknown": true,
               "schema": {
                   "uni": {"type": "list"},
                   "semester": {"type": "list"}
               }},
    "output": {"type": "dict",
               "schema": {
                   "format": {"type": "string", "allowed": ["xml", "json", "csv"]}
               }
    }
}
```

Example JSON request:

```json
'{"input":{"description":"description of the reference course","goals":"learn how to learn"},"output":{"format":"json"},"filter":{"semester":["winter"]}}'
```

Example GET request:

```
http://[host]:[port]/score/compute?input={"description":"description of the reference course","goals":"learn how to learn"}&output={"format":"json"}&filter={"semester":["summer"],"uni":["Zil"]}
```
