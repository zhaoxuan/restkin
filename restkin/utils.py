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

__all__ = [
    'decode_hex_number'
]


class HexDecodeError(ValueError):
    def __init__(self, field, message):
        self.field = field
        self.message = message

    def __repr__(self):
        return ('<HexDecodeError field=%s,message=%s>' % self.field,
                self.message)


def decode_hex_number(field, value):
    try:
        value = int(value, 16)
    except ValueError, e:
        raise HexDecodeError(field=field, message=e.message)

    return value
