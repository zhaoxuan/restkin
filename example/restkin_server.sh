#! /bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR/../
echo 'Start restkin server at 6956'
echo 'Connect to zipkin scribe server at localhost:9410'
echo 'More info: ./bin/restkin-api -help'
./bin/restkin-api --scribe=tcp:localhost:9410