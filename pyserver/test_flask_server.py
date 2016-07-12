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
    def test_post_trip(self):
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

#def test_fail():
#    assert False