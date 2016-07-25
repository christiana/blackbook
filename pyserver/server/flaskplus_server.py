#!/usr/bin/env python

import time
import help_text
import pyserver.costsplitter.trip_manager
import flask
import httplib
from flask.ext.restplus import Api, Resource, fields
import flask.ext.restplus
import pyserver.costsplitter.trip_app 


api = Api(pyserver.costsplitter.trip_app.app, version='0.1', title='Svarteboka API',
    description='''\
A tool for keeping track of expenses on group trips. 
See https://github.com/christiana/blackbook
    ''',
    validate=True
)

ns = api.namespace('', description='TRIP operations')
app = pyserver.costsplitter.trip_app.app
app.trips = pyserver.costsplitter.trip_manager.TripManager()


class DebuggedDate(fields.Date):
    def __init__(self, **kwargs):
        super(DebuggedDate, self).__init__(**kwargs)
        print "**DebuggedDate** ", "created"
        pass
    def format(self, value):
        print "**DebuggedDate** ", "format"
        return super(DebuggedDate, self).format(value)
        pass

id_model = api.model('Id', {
    'id': fields.Integer(readOnly=True, description='Unique identifier')
    })
#id_list_model = api.model('IdList', [])

trip_model = api.model('Trip', {
    'id': fields.Integer(readOnly=True, description='Unique identifier'),
    'name': fields.String(),
    'description': fields.String(),
    'date': fields.Date()
    })
person_model = api.model('Person', 
    {
    'id': fields.Integer(readOnly=True, description='Unique identifier, auto-generated if not input during creation'),
    'name': fields.String(),
    'alias': fields.String(description='Short name'),
    'weight': fields.Float(description='How much of the total should be paid by the person', 
                           default=1,
                           min=1E-2,
                           max=1E2),
    'balance': fields.Float(readOnly=True, description='How much should the person pay or get back.')
    },
    description='One person in the context of a trip.'
    )
payment_model = api.model('Payment', {
    'id': fields.Integer(readOnly=True, description='Unique identifier, auto-generated by server'),
    'type': fields.String(description='''
                          gives the type of payment. 
                          type=split: Amount should be split among all participants according to weight.
                          type=debt: participants owes the creditor the given amount.''',
                          enum=['split', 'debt']),
    'creditor': fields.Integer(description='The `Person` who should be paid back.'),
    'description': fields.String(),
    'amount': fields.Float(description='''
                            The amount of money paid, should be split among participants and paid back to creditor.''',
                            default=0,
                            min=0),
    'participants': fields.List(fields.Integer(), description='''
                                `Persons` part of the payment. 
                                They owe the creditor a sum according to the given type and amount.'''),
    'currency': fields.String(description='The name of the currency used. (EUR, NOK, ...)'),
    'rate': fields.Float(description='The conversion rate from the given amount to the default currency.', 
                         default=1,
                         min=1E-5,
                         max=1E5),
    'date': fields.Date()
    })



###############################################################################
@app.errorhandler(httplib.NOT_FOUND)
def handle_NOT_FOUND(error):
    print "NOT_FOUND ERROR: ", error
    return flask.make_response(flask.jsonify({'error': 'Not found',
                                              'details': str(error)}), 
                               httplib.NOT_FOUND)

@app.errorhandler(httplib.BAD_REQUEST)
def handle_BAD_REQUEST(error):
    print "BADREQUEST ERROR: ", error
    return flask.make_response(flask.jsonify({'error': 'Bad request',
                                              'details': str(error)}), 
                               httplib.BAD_REQUEST)

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def handle_INTERNAL_SERVER_ERROR(error):
    print "INTERNAL ERROR: ", error
    return flask.make_response(flask.jsonify({'error': 'Internal server error',
                                              'details': str(error)}), 
                               httplib.INTERNAL_SERVER_ERROR)

@app.errorhandler(httplib.METHOD_NOT_ALLOWED)
def handle_METHOD_NOT_ALLOWED(error):
    return flask.make_response(flask.jsonify({'error': 'Method not allowed',
                                              'details': str(error)}), 
                               httplib.METHOD_NOT_ALLOWED)
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
    'deprecated - delete'
    head = "<head><title>Svarteboka</title></head>"
    reply = "<html>" + head + help_text.getHelpPageBody() +"</html>"
    return reply

################## TRIPS BEGIN ##############################################
@ns.route('/trips')
class Trips(Resource):
    @ns.doc('list_trips')
    #@ns.marshal_with(id_list_model)
    @api.response(200, 'Success: json list of trip_id')
    def get(self):
        'Get a list of the available `Trip` objects.'
        trips = app.trips.get_trips()
        return trips
    @ns.expect(trip_model)
    @ns.marshal_with(id_model, code=httplib.CREATED)
    def post(self):
        #print '------------date', flask.ext.restplus.inputs.date(flask.request.json['date'])
        'Add a new `Trip`. If no id is given, the server will create one.'
        id = app.trips.add_trip(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<int:trip_id>')
@ns.param('trip_id', 'The trip identifier')
@ns.response(httplib.NOT_FOUND, 'Trip not found')
class Trip(Resource):
    @ns.marshal_with(trip_model)
    def get(self, trip_id):
        'Get a `Trip` object.'
        trip = get_trip(trip_id)
        return trip.get_info()
    @ns.expect(trip_model)
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def put(self, trip_id):
        'Update a `Trip` object.'
        trip = get_trip(trip_id)
        trip.set_info(flask.request.json)
        return {'id': trip_id}, httplib.ACCEPTED
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def delete(self, trip_id):
        'Delete a `Trip` object.'
        trip = get_trip(trip_id)
        app.trips.remove_trip(trip_id)
        return {'id': trip_id}, httplib.ACCEPTED
################## TRIPS END ##############################################

################## PERSONS BEGIN ##############################################
@ns.route('/trips/<int:trip_id>/persons')
@ns.param('trip_id', 'The trip identifier')
@ns.response(httplib.NOT_FOUND, 'Trip not found')
class Persons(Resource):
    @ns.doc('list_persons')
    @api.response(httplib.OK, 'Success: json list of person_id')
    def get(self, trip_id):
        'Get a list of the available `Person` objects.'
        trip = get_trip(trip_id)
        persons = trip.get_persons()
        return persons
    @ns.doc('create_persons')
    @ns.expect(person_model)
    @ns.marshal_with(id_model, code=httplib.CREATED)
    def post(self, trip_id):
        'Add a new `Person`. If no id is given, the server will create one.'
        trip = get_trip(trip_id)
        id = trip.add_person(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<int:trip_id>/persons/<int:person_id>')
@ns.param('trip_id', 'The trip identifier')
@ns.param('person_id', 'The person identifier')
@ns.response(httplib.NOT_FOUND, 'Trip/Person not found')
class Person(Resource):
    @ns.marshal_with(person_model)
    def get(self, trip_id, person_id):
        'Get a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        return person
    @ns.expect(person_model)
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def put(self, trip_id, person_id):
        'Update a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        person = flask.request.json
        person['id'] = person_id
        trip.update_person(person)
        return {'id': person_id}, httplib.ACCEPTED
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def delete(self, trip_id, person_id):
        'Delete a `Person` object.'
        trip = get_trip(trip_id)
        person = get_person(trip_id, person_id)
        trip.remove_person(person_id)
        return {'id': person_id}, httplib.ACCEPTED
################## PERSONS END ##############################################

################## PAYMENTS BEGIN ##############################################
@ns.route('/trips/<int:trip_id>/payments')
@ns.param('trip_id', 'The trip identifier')
@ns.response(httplib.NOT_FOUND, 'Trip not found')
class Payments(Resource):
    @api.response(httplib.OK, 'Success: json list of payment_id')
    def get(self, trip_id):
        'Get a list of the available `Payment` objects.'
        trip = get_trip(trip_id)
        payments = trip.get_payments()
        return payments
    @ns.expect(payment_model)
    @ns.marshal_with(id_model, code=httplib.CREATED)
    def post(self, trip_id):
        'Add a new `Payment`. The id will be auto-generated.'
        trip = get_trip(trip_id)
        id = trip.add_payment(flask.request.json)
        return {'id': id}, httplib.CREATED

@ns.route('/trips/<int:trip_id>/payments/<int:payment_id>')
@ns.param('trip_id', 'The trip identifier')
@ns.param('payment_id', 'The payment identifier')
@ns.response(httplib.NOT_FOUND, 'Trip/Payment not found')
class Payment(Resource):
    @ns.marshal_with(payment_model)
    def get(self, trip_id, payment_id):
        'Get a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        return payment
    @ns.expect(payment_model)
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def put(self, trip_id, payment_id):
        'Update a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        payment = flask.request.json
        payment['id'] = payment_id
        trip.update_payment(payment)
        return {'id': payment_id}, httplib.ACCEPTED
    @ns.marshal_with(id_model, code=httplib.ACCEPTED)
    def delete(self, trip_id, payment_id):
        'Delete a `Payment` object.'
        trip = get_trip(trip_id)
        payment = get_payment(trip_id, payment_id)
        trip.remove_payment(payment_id)
        return {'id': payment_id}, httplib.ACCEPTED
################## PAYMENTS END ##############################################


if __name__ == '__main__':
    app.run(debug=True)