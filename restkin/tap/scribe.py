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

import os
from twisted.internet import reactor

from twisted.application.service import MultiService
from twisted.internet.endpoints import serverFromString

from twisted.web.client import Agent, HTTPConnectionPool

from restkin.tap.utils import BaseOptions

from restkin.scribe import RESTKinHandler

from scrivener import ScribeServerService

from txKeystone import KeystoneAgent


class Options(BaseOptions):
    name = 'restkin-scribe'
    optParameters = [
        ["port", "p", "tcp:0",
         "Port to listen on for the RESTKin Scribe Collector"],
        ["restkin-url", None, "http://localhost:6956/v1.0/tenantId/trace",
         "HTTP(S) URL for posting RESTkin traces."]]


def makeService(config):
    s = MultiService()

    keystone_url = os.getenv(
        'KEYSTONE_URL',
        'https://identity.api.rackspacecloud.com/v2.0/tokens')

    keystone_user = os.getenv('KEYSTONE_USER')
    keystone_pass = os.getenv('KEYSTONE_PASS')

    agent = Agent(reactor, pool=HTTPConnectionPool(reactor, persistent=True))
    if keystone_user and keystone_pass:
        agent = KeystoneAgent(
            agent,
            keystone_url, (keystone_user, keystone_pass))

    handler = RESTKinHandler(agent, config['restkin-url'])

    scribe_service = ScribeServerService(
        serverFromString(reactor, config['port']),
        handler)
    scribe_service.setServiceParent(s)

    return s
