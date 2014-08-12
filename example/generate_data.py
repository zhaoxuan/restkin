import math
import time
import json
import random

def timestamp():
    return math.trunc(time.time() * 1000 * 1000)

def _uniq_id():
    """
    Create a random 64-bit signed integer appropriate
    for use as trace and span IDs.

    XXX: By experimentation zipkin has trouble recording traces with ids
    larger than (2 ** 56) - 1

    @returns C{int}
    """
    return random.randint(0, (2 ** 56) - 1)

def hex_str(n):
    return '%0.16x' % (n,)

timestamp = timestamp()
 
host = {"ipv4": "2130706433", "port": 80, "service_name": "restkin"}

data = [{
    "span_id": hex_str(_uniq_id()),
    "trace_id": hex_str(_uniq_id()),
    "name": "GET",
    "annotations": [
        {"type": "timestamp", "key": "cs", "value": timestamp, "host": host},
        {"type": "string", "key": "name", "value": "zhaoxuan", "host": host},
        {"type": "timestamp", "key": "cr", "value": timestamp + 30000, "host": host}
    ]
}]

f = open('./json_data', 'w')
f.write(json.dumps(data))
f.close()