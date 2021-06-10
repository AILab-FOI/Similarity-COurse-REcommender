# Similarity-COurse-REcommender

This is an implementation of the server-side service of a model for finding similar courses from a set of courses based on the provided reference course attribute values (its description and its goals). Predefined set of courses can be filtered, and the output of the process can be in various formats.

## TOC

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Similarity-COurse-REcommender](#similarity-course-recommender)
	- [TOC](#toc)
	- [How to Run it](#how-to-run-it)
	- [API Request Template](#api-request-template)
	- [Data Sources](#data-sources)

<!-- /TOC -->

## How to Run it

```bash
usage: api.py [-h] [-d] [--host [HOST]] [--port [PORT]]

optional arguments:
  -h, --help     show this help message and exit
  -d             Debug mode
  --host [HOST]  Specify host for server to run on. DEFAULT: 0.0.0.0
  --port [PORT]  Specify port for server to run on. DEFAULT: 50021
```

## API Request Template

In order to provide a valid API request to the `http://[host]:[port]/score/compute` gateway, the GET, POST, or JSON arguments must conform to the following template:

```json
{
    "input": {"type": "dict",
              "required": true,
              "schema": {
                  "description": {"type": "string", "required": true},
                  "goals": {"type": "string", "required": true}
              }},
    "data": {"type": "dict",
             "schema": {
                 "source": {"type": "string"}
             }},
    "filter": {"type": "dict", "allow_unknown": true,
               "schema": {
                   "uni": {"type": "list"},
                   "semester": {"type": "list"}
               }},
    "output": {"type": "dict",
               "schema": {
                   "format": {"type": "string", "allowed": ["xml", "json", "csv"]}
               }}
}
```

Example JSON request:

```json
{"input":{"description":"description of the reference course","goals":"learn how to learn"},"output":{"format":"json"},"filter":{"semester":["winter"]}}
```

Example GET request:

```
http://<host>:<port>/score/compute?input={"description":"description of the reference course","goals":"learn how to learn"}&output={"format":"json"}&filter={"semester":["summer"],"uni":["Zil"]}
```

All the data stored in the connected database can be fetched sing endpoint `http://[host]:[port]/score/fetchdata`. If no output format is provided (following the above template), then the data are returned as JSON.

## Data Sources

The data stored in the included database are copied from the publicly available course descriptions of University of Žilina and Graz University of Technology.
