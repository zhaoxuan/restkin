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
from twisted.web.resource import Resource, NoResource
from tryfer.trace import Trace, Annotation, Endpoint


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
        return TenantResource(path)


class TenantResource(Resource):
    def __init__(self, tenant_id):
        Resource.__init__(self)
        self._tenant_id = tenant_id

    def getChild(self, path, request):
        if path == 'trace':
            return TraceResource()

        return NoResource()


class TraceResource(Resource):
    """
    TraceResource is responsible for taking POST requests and converting
    the JSON output to a scribe log.
    """
    def render_POST(self, request):
        request.responseHeaders.setRawHeaders(
            'content-type', ['application/json'])

        body = request.content.read()

        for json_span in json.loads(body):
            trace_id = int(json_span['trace_id'], 16)
            span_id = int(json_span['span_id'], 16)
            parent_span_id = json_span.get('parent_span_id')

            if parent_span_id:
                parent_span_id = int(parent_span_id, 16)

            t = Trace(json_span['name'], trace_id, span_id, parent_span_id)

            for json_annotation in json_span['annotations']:
                annotation = Annotation(
                    json_annotation['key'],
                    json_annotation['value'],
                    json_annotation['type'])

                host = json_annotation.get('host')
                if host:
                    annotation.endpoint = Endpoint(
                        host['ipv4'], host['port'], host['service_name'])

                t.record(annotation)

        return json.dumps({'ok': True})
