#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export FLASK_APP=$DIR/server/flask_server.py

flask run --port 27222