import BaseHTTPServer
import server.server
import costsplitter.trip_manager
import threading
import time
import datetime
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
        r = requests.get(self.url() + '/')
        #print "got response from server:"
        #print r.text
        assert 'Black Book' in r.text    

    @server_call
    def test_server_get_trips(self):
        r = requests.get(self.url() + '/trips')
        print "got response from server:"
        #print r.json()
        #print r.text
        assert len(r.json())==0

    @server_call
    def test_server_post_trip(self):
        trip_info = {'id':'trip1'}
        r = requests.post(self.url() + '/trips', data=json.dumps(trip_info))
        print "got response from server:"
        print r.json()
        r = requests.get(self.url() + '/trips')
        print "got response from server:"
        print r.json()
        assert len(r.json())==1
        assert 'trip1' in r.json()

    @server_call
    def t_est_server_get_nonexistent_trip(self):
        trip_id = 'bad_trip'
        r = requests.get(self.url()+'/trips/'+trip_id)
        print "got response from server:"
        print r.json()
#        assert len(r.json())==1
#        assert 'trip1' in r.json()
        
    @server_call
    def t_est_server_put_post_get_trip(self):
        trip_info = {'id':'trip1'}
        r = requests.post(self.url()+'/trips', 
                          data=json.dumps(trip_info))
        trip_id = r.json()['id']

        trip_info = {'id': trip_id,
                     'name': "trip name",
                     'description': 'This is a trip',
                     'date': datetime.date.today().isoformat()}
        r = requests.put(self.url()+'/trips/'+trip_id, 
                         data=json.dumps(trip_info))
        
        r = requests.get(self.url()+'/trips/'+trip_id)
        print "got response from server:"
        print r.json()
#        assert len(r.json())==1
#        assert 'trip1' in r.json()

    def url(self):
        return 'http://localhost:%i' % server.server.PORT_NUMBER
        
