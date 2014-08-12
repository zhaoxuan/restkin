# Copyright 2012 Rackspace Hosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from twisted.web import http
from twisted.python import log
from twisted.web.resource import Resource, NoResource
from tryfer.trace import Trace, Annotation, Endpoint

from restkin.utils import decode_hex_number


class RProxyWrapper(Resource):
    rp_error_to_http_code = {
        'NR-1000': http.UNAUTHORIZED,
        'NR-1001': http.UNAUTHORIZED,
        'NR-1002': http.UNAUTHORIZED,
        'NR-5000': http.INTERNAL_SERVER_ERROR,
        'NR-2000': 429  # httpbis - To Many Requests
    }

    def __init__(self, wrapped):
        Resource.__init__(self)
        self._wrapped = wrapped

    def render(self, request):
        headers = request.requestHeaders
        rp_error_code = headers.getRawHeaders('X-RP-Error-Code')[0]
        rp_error_response = headers.getRawHeaders('X-RP-Error-Message')[0]

        request.setResponseCode(
            self.rp_error_to_http_code.get(
                rp_error_code, http.INTERNAL_SERVER_ERROR))

        request.responseHeaders.setRawHeaders(
            'Content-Type', ['application/json'])

        return json.dumps({'ok': False,
                           'error_code': rp_error_code,
                           'error_message': rp_error_response})

    def getChild(self, path, request):
        if request.requestHeaders.hasHeader('X-RP-Error-Code'):
            return self

        return self._wrapped.getChild(path, request)


class RootResource(Resource):
    def getChild(self, path, request):
        if path == 'v1.0':
            return VersionResource()

        return NoResource()


class VersionResource(Resource):
    def getChild(self, path, request):
        if path == 'trace':
            return TraceResource()

        return NoResource()

## useless TenantId, so I annotate this code
## POST API from /v1.0/<tenantId>/trace
## to /v1.0/trace

# class TenantResource(Resource):
#     def __init__(self, tenant_id):
#         Resource.__init__(self)
#         self._tenant_id = tenant_id

#     def getChild(self, path, request):
#         if path == 'trace':
#             return TraceResource()

#         return NoResource()


class TraceResource(Resource):
    """
    TraceResource is responsible for taking POST requests and converting
    the JSON output to a scribe log.

    Response formats:

    Success or partial failure:

    {"succeeded": numberOfSucesfullyInsertedTraces,
     "failed": numberOfTracesWhichFailedInsertion}

    Failure due to invalid body:

    {"error": "Error message"}
    """
    def render_POST(self, request):
        print "For CORS by john"

        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST')

        request.responseHeaders.setRawHeaders(
            'content-type', ['application/json'])

        body = request.content.read()

        try:
            spans = json.loads(body)
        except ValueError:
            log.err(None, 'Failed to decode request body')
            msg = 'Could not decode request body (invalid JSON)'
            return json.dumps({'error': msg})

        succeeded, failed = 0, 0

        for json_span in spans:
            trace_id = None
            span_id = None

            try:
                trace_id = decode_hex_number('trace_id', json_span['trace_id'])
                span_id = decode_hex_number('span_id', json_span['span_id'])
                parent_span_id = json_span.get('parent_span_id', None)

                if parent_span_id is not None:
                    parent_span_id = decode_hex_number('parent_span_id',
                                                       parent_span_id)

                t = Trace(json_span['name'], trace_id, span_id, parent_span_id)

                for json_annotation in json_span['annotations']:
                    annotation = Annotation(
                        json_annotation['key'],
                        json_annotation['value'],
                        json_annotation['type'])

                    host = json_annotation.get('host', None)

                    if host:
                        annotation.endpoint = Endpoint(
                            host['ipv4'], host['port'], host['service_name'])

                    t.record(annotation)
                    succeeded = succeeded + 1
            except Exception:
                log.err(None,
                        'Failed to insert a trace: trace_id=%r,span_id=%r' %
                        (trace_id, span_id))

                failed = failed + 1
                continue

        return json.dumps({'succeeded': succeeded, 'failed': failed})
