#! /bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo 'Generate json post data'
python $DIR/generate_data.py
echo 'Post example/json_data to restkin server'
curl -H "Content-Type: application/json" -X POST -d @$DIR/json_data http://117.185.16.31:6956/v1.0/trace
