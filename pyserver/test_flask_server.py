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
        #print "self.app", self.app
        #print "server.flask_server.app.test_client()", server.flask_server.app.test_client()
        #self.threaded_server = ThreadedServer()
        #self.threaded_server.start()
        try:
            return func(self)
        finally:
            print "resetting counter"
            server.flask_server.app.counter = 0
            #self.threaded_server.stop()
    return func_wrapper

class TestFlaskServer:
    @server_call
    def test_index(self):    
        r = self.client.get('/')
        #print 'response: ', r.data
        assert 'Black Book' in r.data

    @server_call
    def test_get_trips(self):    
        r = self.client.get('/trips')
        print 'response: ', r.data
        assert 'Black Book' in r.data    

#def test_fail():
#    assert False