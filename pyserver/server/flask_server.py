#!/usr/bin/env python

import time
import help_text
import pyserver.costsplitter.trip_manager
#from flask import Flask, jsonify
import flask

app = flask.Flask(__name__)
#app.object = "Hello, World!"
#app.counter = 0
app.trips = pyserver.costsplitter.trip_manager.TripManager()


@app.route('/')
def handle_index():
    head = "<head><title>Svarteboka</title></head>"
    reply = "<html>" + head + help_text.getHelpPageBody() +"</html>"
    return reply

@app.route('/trips', methods=['GET'])
def handle_get_trips():
    ""
    trips = app.trips.get_trips()
    #print "handle_get_trips", trips
    return flask.jsonify(trips)

@app.route('/trips', methods=['POST'])
def handle_post_trip():
    #print "incomingd: ", flask.request.data
    #print "incomingj: ", flask.request.json
    if not flask.request.json or not 'id' in flask.request.json:
        flask.abort(400)
    id = app.trips.add_trip(flask.request.json)
    return flask.jsonify({'id': id}), 201

if __name__ == '__main__':
    app.run(debug=True)