#!/usr/bin/env python
#
#
# based on https://wiki.python.org/moin/BaseHttpServer
#

import BaseHTTPServer
import time
import help_text
import pyserver.costsplitter.trip_manager
import json
import StringIO
import re

#
#
#
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    Interface to server, see help_text.py for description
    '''
    def __init__(self, *args, **kwargs):
        #print "-------**************-------------- init"
        #self.trips = pyserver.costsplitter.trip_manager.TripManager()
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def print_info(self):
        print '>>>incoming: ', self.command, ' - ', self.path
    
    def path_matches(self, expr):
        retval = re.match(expr, self.path)
        if retval:
            print "************HIT ", expr, " vs ", self.path
        else:
            print "****--------NO HIT ", expr, " vs ", self.path
        return retval 
    
#    def get_trip_id(self):
#        p = self.path_matches('/trips/(.*)(?<!/)$')
#        if p:
#            print "groups", p.groups()
#            return True

    def do_HEAD(self):
        self.print_info()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        """Respond to a GET request."""
        self.print_info()
#        if self.path=='/':
        if self.path_matches('/$'):
            return self.handle_get_root()
        if self.path_matches('/trips$'):
            return self.handle_get_trips()
        if self.path_matches('/trips/.*(?<!/)$'):
            return self.handle_get_trip()
        return self.handle_failure()

        if self.get_group_type()=='persons':
            return self.handle_group_persons()
        if self.get_group_type()=='payments':
            return self.handle_group_payments()
        if self.get_group_type() is not None:
            return self.handle_failure()
        return self.handle_get_group_trips()

    def do_POST(self):
        """Respond to a POST request."""
        self.print_info()
        if self.path_matches('/trips$'):
        #if self.path=='/trips':
            return self.handle_post_trip()
            
    def handle_post_trip(self):
        #indata = StringIO.StringIO(self.rfile).getvalue()
        #print "indata:", str(indata)
        length = int(self.headers['content-length'])
        #print "indata len:", length
        #indata = self.rfile.read(length)
        indata = json.loads(self.rfile.read(length))
        print "json indata:", indata
        print ""
        trips = self.server.trips.get_trips() 
        
        trip_id = indata['id'] 
        if trip_id in trips:
            return self.handle_failure("trip id %s already exists"%trip_id)
        
        self.server.trips.add_trip(trip_id)        
               
        trips = self.server.trips.get_trips()
        print "handle_post_trip", trips
               
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(json.dumps(indata))
    
    def handle_get_trip(self):
        id = self.get_trip_id()
                            
    def handle_get_group_trips(self):
        if self.path == '/trips':
            return self.handle_get_trips()
        trip_name = self.get_trip_name()
        if trip_name is None:
            return self.handle_failure()
    
    def handle_group_persons(self):
        pass

    def handle_group_payments(self):
        pass
    
    def get_trip_id(self):
        'get the trip id/name'
        comps = self.path.split('/')
        if len(comps)>=3 and comps[1]=='trips':
            return comps[2]
        return None

    def get_group_type(self):
        'return group type, such as person or payment'
        comps = self.path.split('/')
        print "comps", comps
        if len(comps)>=4 and comps[1]=='trips':
            return comps[3]
        return None

    def get_group_name(self):
        'return name of group, either id of person or id of payment'
        comps = self.path.split('/')
        if len(comps)>=5 and comps[1]=='trips':
            return comps[4]
        return None
        
#    def split(self, path):
#        comps = path.split('/')
#        retval = {}
#        retval['trip_name'] = comps[1]
#        retval['group_name'] = comps[2]
#        retval['group_value'] = comps[3]

    def handle_get_root(self):
        ""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Black Book.</title></head>")
        self.wfile.write(help_text.getHelpPageBody())        
        self.wfile.write("</html>")
    
    def handle_get_trips(self):
        ""
        trips = self.server.trips.get_trips()
        print "handle_get_trips", trips
        
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(json.dumps(trips))
    
    def handle_failure(self):   
        self.send_response(401)
        self.end_headers()



###########################################################
HOST_NAME = ''
PORT_NUMBER = 23234 # obscurity-based number
    
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RequestHandler)
    httpd.trips = pyserver.costsplitter.trip_manager.TripManager()
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)    
    
    

