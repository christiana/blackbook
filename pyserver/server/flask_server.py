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

###############################################################################
@app.errorhandler(httplib.NOT_FOUND)
def handle_NOT_FOUND(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), httplib.NOT_FOUND)

@app.errorhandler(httplib.BAD_REQUEST)
def handle_BAD_REQUEST(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), httplib.BAD_REQUEST)

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def handle_INTERNAL_SERVER_ERROR(error):
    return flask.make_response(flask.jsonify({'error': 'Internal server error'}), httplib.INTERNAL_SERVER_ERROR)

@app.errorhandler(httplib.METHOD_NOT_ALLOWED)
def handle_METHOD_NOT_ALLOWED(error):
    return flask.make_response(flask.jsonify({'error': 'Method not allowed'}), httplib.METHOD_NOT_ALLOWED)
###############################################################################

@app.route('/')
def handle_index():
    head = "<head><title>Svarteboka</title></head>"
    reply = "<html>" + head + help_text.getHelpPageBody() +"</html>"
    return reply

################## TRIPS BEGIN ##############################################
@app.route('/trips', methods=['GET'])
def handle_get_trips():
    trips = app.trips.get_trips()
    return flask.jsonify(trips)

@app.route('/trips', methods=['POST'])
def handle_post_trip():
    id = app.trips.add_trip(flask.request.json)
    return flask.jsonify({'id': id}), httplib.CREATED

def get_trip(trip_id):
    trip = app.trips.get_trip(trip_id)
    if not trip:
        flask.abort(httplib.NOT_FOUND)
    return trip

@app.route('/trips/<string:trip_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_trip(trip_id):
    trip = get_trip(trip_id)
    if flask.request.method=='PUT':
        trip.set_info(flask.request.json)
        return flask.jsonify({'id': trip_id}), httplib.ACCEPTED
    if flask.request.method=='GET':
        return flask.jsonify(trip.get_info())
    if flask.request.method=='DELETE':
        app.trips.remove_trip(trip_id)
        return flask.jsonify({'id': trip_id}), httplib.ACCEPTED
################## TRIPS END ##############################################

################## PERSONS BEGIN ##############################################
@app.route('/trips/<trip_id>/persons', methods=['GET'])
def handle_get_persons(trip_id):
    trip = get_trip(trip_id)
    persons = trip.get_persons()
    return flask.jsonify(persons)

@app.route('/trips/<trip_id>/persons', methods=['POST'])
def handle_post_person(trip_id):
    trip = get_trip(trip_id)
    id = trip.add_person(flask.request.json)
    return flask.jsonify({'id': id}), httplib.CREATED

@app.route('/trips/<trip_id>/persons/<person_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_person(trip_id, person_id):
    trip = get_trip(trip_id)
    person = trip.get_person(person_id)
    if not person:
        flask.abort(httplib.NOT_FOUND)
    if flask.request.method=='PUT':
        person = flask.request.json
        person['id'] = person_id
        trip.add_person(person)
        return flask.jsonify({'id': person_id}), httplib.ACCEPTED
    if flask.request.method=='GET':
        return flask.jsonify(person)
    if flask.request.method=='DELETE':
        trip.remove_person(person_id)
        return flask.jsonify({'id': person_id}), httplib.ACCEPTED
################## PERSONS END ##############################################

################## PAYMENTS BEGIN ##############################################
@app.route('/trips/<trip_id>/payments', methods=['GET'])
def handle_get_payments(trip_id):
    trip = get_trip(trip_id)
    payments = trip.get_payments()
    return flask.jsonify(payments)

@app.route('/trips/<trip_id>/payments', methods=['POST'])
def handle_post_payment():
    trip = get_trip(trip_id)
    id = trip.add_payments(flask.request.json)
    return flask.jsonify({'id': id}), httplib.CREATED

@app.route('/trips/<trip_id>/payments/<payment_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_payment(trip_id, payment_id):
    trip = get_trip(trip_id)
    payment = trip.get_payment(payment_id)
    if not payment:
        flask.abort(httplib.NOT_FOUND)
    if flask.request.method=='PUT':
        payment = flask.request.json
        payment['id'] = payment_id
        trip.add_payment(payment)
        return flask.jsonify({'id': payment_id}), httplib.ACCEPTED
    if flask.request.method=='GET':
        return flask.jsonify(payment)
    if flask.request.method=='DELETE':
        trip.remove_payment(payment_id)
        return flask.jsonify({'id': payment_id}), httplib.ACCEPTED
################## PAYMENTS END ##############################################


if __name__ == '__main__':
    app.run(debug=True)