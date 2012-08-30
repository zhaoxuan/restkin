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

import sys

from twisted.python.usage import Options
from restkin import __version__


class BaseOptions(Options):
    name = None

    def getSynopsis(self):
        return 'Usage: {0} [options]'.format(self.name)

    def opt_h(self):
        return self.opt_help()

    def opt_version(self):
        """
        Display versions and exit.
        """
        from twisted import copyright
        print '\n'.join([
            '{0} version: {1}'.format(self.name, __version__),
            'Twisted version {0}'.format(copyright.version)])
        sys.exit(0)
