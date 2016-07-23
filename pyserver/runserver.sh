#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#export FLASK_APP=$DIR/server/flask_server.py
#export FLASK_APP=$DIR/server/restplus_example.py

export FLASK_APP=$DIR/server/flaskplus_server.py
#export TRIP_DB=sqlite:///:memory:
export TRIP_DB=sqlite:///$DIR/trips.db


flask run --host 0.0.0.0 --port 27222
