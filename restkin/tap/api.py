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

from twisted.web import server
from twisted.application import strports
from twisted.application.service import MultiService

from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString

from scrivener import ScribeClient
from tryfer.tracers import ZipkinTracer, push_tracer

from restkin.tap.utils import BaseOptions

from restkin.api import RootResource, RProxyWrapper


class Options(BaseOptions):
    name = 'restkin-api'

    optParameters = [
        ["port", "p", "tcp:6956",
         "Port to listen on for RESTkin HTTP API requests"],
        ["scribe", None, "tcp:localhost:1463",
         "endpoint string description for where to connect to scribe"]]

    optFlags = [["rproxy", "r", "Use node-rproxy for authentication."]]


def makeService(config):
    s = MultiService()


    # ZipkinTracer(
    #     scribe_client,
    #     category=None,
    #     end_annotations=None,
    #     max_traces=50,
    #     max_idle_time=10,
    #     _reactor=None)
    push_tracer(
        ZipkinTracer(
            ScribeClient(clientFromString(reactor, config['scribe'])), 'zipkin', None, 10, 10, None))

    root = RootResource()

    # if config['rproxy']:
    #     root = RProxyWrapper(root)

    site = server.Site(root)
    site.displayTracebacks = False

    api_service = strports.service(config['port'], site)
    api_service.setServiceParent(s)

    return s
