import datetime
import trip
    
class TripManager:
    '''
    '''
    def __init__(self, root_path = None):
        self.trips = []
    
#    def add_trip(self, name):
#        if name not in self.get_trips():
#            self.trips.append(trip.Trip(name))
#        return name

    def add_trip(self, trip_info):
        if not isinstance(trip_info, dict):
            trip_info = {} # ignore all other inputs
        if 'id' not in trip_info:
            trip_info['id'] = self._generate_unique_trip_id()
        id = trip_info['id']
        entry = self.get_trip(id)
        if not entry: 
            entry = trip.Trip(id)
            self.trips.append(entry)
        entry.set_info(trip_info)
        return id
        
    def remove_trip(self, name):
        self.trips.remove(self.get_trip(name))
    
    def get_trips(self):
        #print "get_trips ", len(self.trips) 
        return [trip.get_info()['id'] for trip in self.trips]
    
    def get_trip(self, id):
        for trip in self.trips:
            if trip.get_info()['id'] == id:
                return trip
        return None
    
    def _generate_unique_trip_id(self):
        i = 0
        while True:
            uid = 'trip%s' % i
            if not self.get_trip(uid):
                return uid
            i = i+1
            
            
         
    
    
    
        
    