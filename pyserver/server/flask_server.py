#!/usr/bin/env python

import time
import help_text
import pyserver.costsplitter.trip_manager
#from flask import Flask, jsonify
import flask
import httplib

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
    trips = app.trips.get_trips()
    return flask.jsonify(trips)

@app.route('/trips', methods=['POST'])
def handle_post_trip():
    if not flask.request.json or not 'id' in flask.request.json:
        flask.abort(httplib.BAD_REQUEST)
    id = app.trips.add_trip(flask.request.json)
    return flask.jsonify({'id': id}), httplib.CREATED

@app.route('/trips/<string:trip_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_trip(trip_id):
    trip = app.trips.get_trip(trip_id)
    print "trip", trip    
    if not trip:
        flask.abort(httplib.NOT_FOUND)
    if flask.request.method=='PUT':
        trip.set_info(flask.request.json)
        return flask.jsonify({'id': trip_id}), httplib.ACCEPTED
    if flask.request.method=='GET':
        return flask.jsonify(trip.get_info())
    if flask.request.method=='DELETE':
        app.trips.remove_trip(trip_id)
        return flask.jsonify({'id': trip_id}), httplib.ACCEPTED

#@app.route('/trips/<trip_id>', methods=['GET'])
#def handle_get_trip(trip_id):
#    trip = app.trips.get_trip(trip_id)    
#    if not trip:
#        flask.abort(httplib.BAD_REQUEST)
#    return flask.jsonify(trip.get_info())

#@app.route('/trips/<trip_id>', methods=['DELETE'])
#def handle_delete_trip(trip_id):
#    trip = app.trips.get_trip(trip_id)    
#    if not trip:
#        flask.abort(httplib.BAD_REQUEST)
#    return flask.jsonify(trip.get_info())

if __name__ == '__main__':
    app.run(debug=True)