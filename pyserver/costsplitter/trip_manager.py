import datetime
import trip
import trip_database
        
class TripManager:
    '''
    Wraps the list of trips in the database, 
    handle create/destroy
    '''
    def __init__(self):
        pass
        
    def add_trip(self, trip_info={}):
        return trip.Trip.create_trip(trip_info)
        
    def remove_trip(self, id):
        self.get_trip(id).remove_trip()
        return id
    
    def get_trips(self):
        return [trip.id for trip in trip_database.Trip.query.all()]
    
    def get_trip(self, id):
        if id not in self.get_trips():
            return None
        return trip.Trip(id)
    
    
            
            
         
    
    
    
        
    