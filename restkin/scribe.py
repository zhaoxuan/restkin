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

from StringIO import StringIO

from zope.interface import implements

from twisted.python import log
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol

from twisted.web.client import FileBodyProducer
from twisted.web.http_headers import Headers

from scrivener.interfaces import ILogHandler


class _BodyReceiver(Protocol):
    def __init__(self, finished):
        self._finished = finished
        self._buffer = []

    def dataReceived(self, data):
        self._buffer.append(data)

    def connectionLost(self, reason):
        self._finished.callback(''.join(self._buffer))


class RESTKinHandler(object):
    implements(ILogHandler)

    category = 'restkin'

    def __init__(self, agent, restkin_url):
        self._agent = agent
        self._restkin_url = restkin_url

    def _log_success(self, response):
        def _do_log(body):
            log.msg(format="Response from RESTKin: %(code)s %(body)s",
                    code=response.code, body=body)

        d = Deferred()
        response.deliverBody(_BodyReceiver(d))
        d.addCallback(_do_log)
        return d

    def log(self, category, message):
        if category != self.category:
            log.msg(format=("Unknown category: %(category)s "
                            "expected %(expected_category)"),
                    category=category,
                    expected_category=self.category)

        d = self._agent.request(
            'POST', self._restkin_url,
            Headers({'Content-Type': ['application/json']}),
            FileBodyProducer(StringIO(message)))

        d.addCallback(self._log_success)
        d.addErrback(log.err, "Unhandled error while posting to RESTKin")
