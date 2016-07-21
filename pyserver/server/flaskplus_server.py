#!/usr/bin/env python

import time
import help_text
import pyserver.costsplitter.trip_manager
import flask
import httplib
from flask.ext.restplus import Api, Resource, fields

app = flask.Flask(__name__)

api = Api(app, version='0.1', title='Svarteboka API',
    description='''\
A tool for keeping track of expenses on group trips. 
See https://github.com/christiana/blackbook
    '''
    ,
    
)

ns = api.namespace('', description='TRIP operations')

trip = api.model('Trip', {
    'id': fields.String(readOnly=False, description='The trip unique identifier, auto-generated if not input during creation'),
    'name': fields.String(),
    'description': fields.String(),
    'date': fields.Date()
})


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


def get_trip(trip_id):
    trip = app.trips.get_trip(trip_id)
    if not trip:
        flask.abort(httplib.NOT_FOUND)
    return trip

def get_person(trip_id, person_id):
    trip = get_trip(trip_id)
    person = trip.get_person(person_id)
    if not person:
        flask.abort(httplib.NOT_FOUND)
    return person

def get_payment(trip_id, payment_id):
    trip = get_trip(trip_id)
    payment = trip.get_payment(payment_id)
    if not payment:
        flask.abort(httplib.NOT_FOUND)
    return payment



#@app.route('/')
def handle_index():
    head = "<head><title>Svarteboka</title></head>"
    reply = "<html>" + head + help_text.getHelpPageBody() +"</html>"
    return reply

################## TRIPS BEGIN ##############################################
@ns.route('/trips')
class Trips(Resource):
    @ns.doc('list_trips')
    def get(self):
        'Get a list of the available `Trip` objects.'
        trips = app.trips.get_trips()
        return trips
    @ns.doc('create_trips')
    @ns.expect(trip)
    def post(self):
        'Add a new `Trip`. If no id is given, the server will create one.'
        id = app.trips.add_trip(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<string:trip_id>')
class Trip(Resource):
    def get(self, trip_id):
        'Get a `Trip` object.'
        trip = get_trip(trip_id)
        return trip.get_info()
    def put(self, trip_id):
        'Update a `Trip` object.'
        trip = get_trip(trip_id)
        trip.set_info(flask.request.json)
        return {'id': trip_id}, httplib.ACCEPTED
    def delete(self, trip_id):
        'Delete a `Trip` object.'
        trip = get_trip(trip_id)
        app.trips.remove_trip(trip_id)
        return {'id': trip_id}, httplib.ACCEPTED
################## TRIPS END ##############################################

################## PERSONS BEGIN ##############################################
@ns.route('/trips/<trip_id>/persons')
class Persons(Resource):
    @ns.doc('list_persons')
    def get(self, trip_id):
        'Get a list of the available `Person` objects.'
        trip = get_trip(trip_id)
        persons = trip.get_persons()
        return persons
    @ns.doc('create_persons')
    #@ns.expect(person)
    def post(self, trip_id):
        'Add a new `Person`. If no id is given, the server will create one.'
        trip = get_trip(trip_id)
        id = trip.add_person(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<trip_id>/persons/<person_id>')
class Person(Resource):
    def get(self, trip_id, person_id):
        'Get a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        return person
    def put(self, trip_id, person_id):
        'Update a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        person = flask.request.json
        person['id'] = person_id
        trip.add_person(person)
        return {'id': person_id}, httplib.ACCEPTED
    def delete(self, trip_id, person_id):
        'Delete a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        trip.remove_person(person_id)
        return {'id': person_id}, httplib.ACCEPTED
################## PERSONS END ##############################################

################## PAYMENTS BEGIN ##############################################
@ns.route('/trips/<trip_id>/payments')
class Payments(Resource):
    def get(self, trip_id):
        'Get a list of the available `Payment` objects.'
        trip = get_trip(trip_id)
        payments = trip.get_payments()
        return payments
    def post(self, trip_id):
        'Add a new `Payment`. If no id is given, the server will create one.'
        trip = get_trip(trip_id)
        id = trip.add_payment(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<trip_id>/payments/<payment_id>')
class Payment(Resource):
    def get(self, trip_id, payment_id):
        'Get a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        return payment
    def put(self, trip_id, payment_id):
        'Update a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        payment = flask.request.json
        payment['id'] = payment_id
        trip.add_payment(payment)
        return {'id': payment_id}, httplib.ACCEPTED
    def delete(self, trip_id, payment_id):
        'Delete a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        trip.remove_payment(payment_id)
        return {'id': payment_id}, httplib.ACCEPTED
################## PAYMENTS END ##############################################


if __name__ == '__main__':
    app.run(debug=True)