#!/usr/bin/env python

import time
import help_text
import pyserver.costsplitter.trip_manager
from flask import Flask

app = Flask(__name__)
#app.object = "Hello, World!"
#app.counter = 0
app.trips = pyserver.costsplitter.trip_manager.TripManager()


@app.route('/')
def handle_index():
    head = "<head><title>Svarteboka</title></head>"
    reply = "<html>" + head + help_text.getHelpPageBody() +"</html>"
    return reply

@app.route('/trips', methods=['GET'])
def handle_get_trips(self):
    ""
    trips = self.server.trips.get_trips()
    print "handle_get_trips", trips
    return trips
    
#    self.send_response(200)
#    self.send_header("Content-type", "text/json")
#    self.end_headers()
#    self.wfile.write(json.dumps(trips))

@app.route('/trips', methods=['POST'])
def handle_post_trip(self):
    length = int(self.headers['content-length'])
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
    
    

if __name__ == '__main__':
    app.run(debug=True)