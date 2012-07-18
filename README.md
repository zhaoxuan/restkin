# restkin

A REST interface for publishing traces to zipkin

## TODO

 - BinaryAnnotations
    The answer to supporting binary annotations to is to allow the JSON API to
    depart from the thrift API and allow concise expression of multiple types of
    annotations.

        {
            "key": <String>,
            "type": <String: bool | int | bytes | timestamp>,
            "value": <appropriate JSON type>,
            "host": {
                "ipv4": <String>,
                "port": <Integer>,
                "service_name": <String>
            }
        }

## API

### POST /trace

Headers:
 * Content-Type: application/json
 * X-Auth-Token: <Auth Token>

Body:

    [
        {
            "trace_id": <64-bit integer>,
            "span_id": <64-bit integer>,
            "parent_id": <64-bit integer>, //optional
            "name": <String>,
            "annotations": [
                {
                    "timestamp": <64-bit integer>, // UTC usec since epoch
                    "value": <String>,
                    "host": { // optional
                        "ipv4": <String>,
                        "port": <Integer>,
                        "service_name": <String>
                    }
                }
            ]
        }
    ]

## Usage

Start server:

    lein ring server

Use curl to add a trace:

    curl -v -d '[{"annotations": [{"timestamp": 1, "value": "crossing", host: {"ipv4": "127.0.0.1", "port": 5000, "service_name": "zoo"}}], "parent_id": 1, "trace_id":1, "name": "zebras", "span_id":2}]' -H "Content-Type: application/json" -H "Accept: application/json" http://localhost:3000/trace

## License

Copyright (C) 2012 FIXME
