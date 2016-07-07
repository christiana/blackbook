import BaseHTTPServer
import server.server
import costsplitter.trip_manager
import threading
import time
import requests
import pytest
import json

class ServerRunner:
    '''
    '''
    def __init__(self):
        self.httpd = None
        self.stopped = False
        self.lock = threading.Lock()
    
    def __call__(self):
        self.lock.acquire()
        if not self.stopped:
            server_class = BaseHTTPServer.HTTPServer
            self.httpd = server_class(('', server.server.PORT_NUMBER), server.server.RequestHandler)
            self.httpd.trips = costsplitter.trip_manager.TripManager()
        self.lock.release()
        print "started server."
        
        self.httpd.serve_forever()

        self.lock.acquire()
        self.httpd = None
        self.lock.release()
        
    def stop(self):
        self.lock.acquire()
        self.stopped = True      
        if self.httpd:
            self.httpd.shutdown()
        self.lock.release()
    
    
class ThreadedServer(threading.Thread):
    '''
    '''
    def __init__(self):
        pass
    def start(self):
        print "************************ starting server..."
        self.runner = ServerRunner()
        self.server_thread = threading.Thread(target=self.runner)
        self.server_thread.start()
    def stop(self):
        print "stopping server..."
        self.runner.stop()
        self.server_thread.join()
        print "************************ stopped server"


def server_call(func):
    '''
    decorator starting and stopping the blackbook server
    '''
    def func_wrapper(self):
        self.threaded_server = ThreadedServer()
        self.threaded_server.start()
        try:
            return func(self)
        finally:
            self.threaded_server.stop()
    return func_wrapper


class TestServer:
    @server_call
    def test_server_get_main_page(self):        
        r = requests.get('http://localhost:%i' % server.server.PORT_NUMBER)
        #print "got response from server:"
        #print r.text
        assert 'Black Book' in r.text    

    @server_call
    def test_server_get_trips(self):
        r = requests.get('http://localhost:%i/trips' % server.server.PORT_NUMBER)
        print "got response from server:"
        #print r.json()
        #print r.text
        assert len(r.json())==0

    @server_call
    def test_server_put_trips(self):
        trip_info = {'id':'trip1'}
        r = requests.post('http://localhost:%i/trips' % server.server.PORT_NUMBER, data=json.dumps(trip_info))
        print "got response from server:"
        print r.json()
        r = requests.get('http://localhost:%i/trips' % server.server.PORT_NUMBER)
        print "got response from server:"
        print r.json()
        assert len(r.json())==1
        assert 'trip1' in r.json()
