restkin
=======

A REST interface for publishing traces to zipkin.

API
===

POST /v1.0/trace
----------------

Headers:
 * ``Content-Type: application/json``
 * ``X-Auth-Token: <Auth Token>`` optional

Body::

    [
        {
            "trace_id": <16-char hex string>,
            "span_id": <16-char hex string>,
            "parent_id": <16-char hex string>, //optional
            "name": <String>,
            "annotations": [
                {
                    "key": <String>,
                    "type": <String: string | bytes | timestamp>,
                    "value": <appropriate JSON type>,
                    "host": {
                        "ipv4": <String>,
                        "port": <Integer>,
                        "service_name": <String>
                    }
                }
            ]
        }
    ]

Dependencies
------------

* Twisted 12.1.0
* https://github.com/racker/scrivener
* https://github.com/racker/tryfer
* https://github.com/racker/node-rproxy (optional)

Running RESTkin-API
-------------------

::

    > ./bin/restkin-api --help
    Usage: restkin-api [options]
    Options:
      -r, --rproxy   node-rproxy will be in front of this service.
      -p, --port=    Port to listen on for RESTkin API requests [default: tcp:6956]
          --scribe=  endpoint string description for where to connect to scribe
                     [default: tcp:localhost:1463]
          --version  Display versions and exit.
          --help     Display this help and exit.

    > ./bin/restkin-api


Running RESTkin-Scribe
----------------------

::

    > ./bin/restkin-scribe --help
    Usage: restkin-scribe [options]
    Options:
      -p, --port=         Port to listen on for the RESTKin Scribe Collector
                          [default: tcp:0]
          --restkin-url=  HTTP(S) URL for posting RESTkin traces. [default:
                          http://localhost:6956/v1.0/trace]
          --version       Display versions and exit.
          --help          Display this help and exit.

    > ./bin/restkin-scribe --restkin-url=http://localhost:6956/v1.0/trace

License
-------
::

    Copyright (C) 2012 Rackspace Hosting, Inc

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
