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

from twisted.application.service import ServiceMaker

RESTkinAPI = ServiceMaker(
        "RESTkin API - A REST interface to tracing with Zipkin",
        "restkin.tap.api",
        "Forward REST requests to Zipkin over scribe.",
        "restkin-api")

RESTKinScribe = ServiceMaker(
        "RESTKin Scribe - A Scribe collector that posts to RESTKin",
        "restkin.tap.scribe",
        "Forward JSON Scribe Logs to RESTKin to be carried on to Zipkin.",
        "restkin-scribe")
