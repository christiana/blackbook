#!/usr/bin/env python
#
#
# based on https://wiki.python.org/moin/BaseHttpServer
#

import BaseHTTPServer
import time
import help_text

#
#
#
#
#
#
#
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    Interface to server, see help_text.py for description
    '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Black Book.</title></head>")
        self.wfile.write(help_text.getHelpPageBody())        
        self.wfile.write("</html>")

    

HOST_NAME = ''
PORT_NUMBER = 23234 # obscurity-based number
    
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RequestHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)    
    
    

