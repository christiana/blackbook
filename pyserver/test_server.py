import BaseHTTPServer
import server.server
import threading
import time
import requests

class ServerRunner:
    def __init__(self):
        self.httpd = None
        self.stopped = False
        self.lock = threading.Lock()
    
    def __call__(self):
        self.lock.acquire()
        if not self.stopped:
            server_class = BaseHTTPServer.HTTPServer
            self.httpd = server_class(('', server.server.PORT_NUMBER), server.server.RequestHandler)
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
    def __init__(self):
        print "starting server..."
        self.runner = ServerRunner()
        self.server_thread = threading.Thread(target=self.runner)
        self.server_thread.start()
    def stop(self):
        print "stopping server..."
        self.runner.stop()
        self.server_thread.join()
        print "stopped server"


def test_server_get_main_page():
    threaded_server = ThreadedServer()
#    time.sleep(3)
    
    r = requests.get('http://localhost:%i' % server.server.PORT_NUMBER)
    print "got response from server:"
    print r.text
    
    assert 'Black Book' in r.text    
#    time.sleep(3)
    threaded_server.stop()

