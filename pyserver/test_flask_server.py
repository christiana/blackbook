import BaseHTTPServer
import server.server
import costsplitter.trip_manager
import threading
import time
import datetime
import requests
import pytest
import json
import server.flask_server
import httplib

def server_call(func):
    '''
    decorator starting and stopping the blackbook server
    '''
    def func_wrapper(self):
        self.client = server.flask_server.app.test_client()
        try:
            return func(self)
        finally:
            #print "resetting counter"
            #server.flask_server.app.counter = 0
            server.flask_server.app.trips = costsplitter.trip_manager.TripManager()
    return func_wrapper

class TestFlaskServer:
    '''
    Test the flask server REST API
    '''
    @server_call
    def test_index(self):    
        r = self.client.get('/')
        #print 'response: ', r.data
        assert 'Black Book' in r.data

    @server_call
    def test_get_trips(self):    
        r = self.client.get('/trips')
        #print 'response: ', r.data
        #print 'response_json', json.loads(r.data)
        assert len(json.loads(r.data))==0

    @server_call
    def test_post_named_trip(self):
        trip_id = 'trip1'
        r = self.client.post('/trips', data=json.dumps({'id':trip_id}), content_type = 'application/json')
        #print "got response from server:"
        #print json.loads(r.data)
        
        r = self.client.get('/trips')
        returned_trips = json.loads(r.data)
        #print "got response from server:"
        #print returned_trips
        assert len(returned_trips)==1
        assert 'trip1' in returned_trips

    @server_call
    def test_post_unnamed_trip(self):
        trip_name = 'A brand new trip'
        r = self.client.post('/trips', data=json.dumps({'name':trip_name}), content_type = 'application/json')
        #print "got response from server:"
        #print json.loads(r.data)
        trip_id = json.loads(r.data)['id']
        
        r = self.client.get('/trips/'+trip_id)
        returned_trip = json.loads(r.data)
        #print "got response from server:"
        #print returned_trip
        assert returned_trip['name'] == trip_name

    @server_call
    def test_get_nonexistent_trip(self):
        trip_id = 'bad_trip'
        r = self.client.get('/trips/'+trip_id)
        #print "got response from server:"
#        print "data : ", help(r)
        #print "status : ", r.status
        #print "status_code : ", r.status_code
        #print "data : ", r.data
        assert r.status_code == httplib.NOT_FOUND

    @server_call
    def test_post_put_trip(self):
        trip_id = 'trip1'
        r = self.client.post('/trips', 
                             data=json.dumps({'id':trip_id}), 
                             content_type = 'application/json')
        
        input_trip = {'id':trip_id, 'description':'descriptive string'}
        r = self.client.put('/trips/trip1', 
                            data=json.dumps(input_trip),
                            content_type = 'application/json')

        r = self.client.get('/trips/trip1')
        returned_trip = json.loads(r.data)
        assert returned_trip['id'] == input_trip['id']
        assert returned_trip['description'] == input_trip['description']

    @server_call
    def test_delete_trip(self):
        r = self.client.post('/trips', 
                             data=json.dumps({'id':'trip1'}), 
                             content_type = 'application/json')

        r = self.client.get('/trips')
        returned_trips = json.loads(r.data)
        assert len(returned_trips)==1
        
        r = self.client.delete('/trips/trip1')

        r = self.client.get('/trips')
        returned_trips = json.loads(r.data)
        assert len(returned_trips)==0
        
