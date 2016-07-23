import datetime
import trip
import trip_database
    
    
class TripManager:
    '''
    Wraps the list of trips in the database, 
    handle create/destroy
    '''
    def __init__(self):
        self.trip_db = trip_database.TripDB(table=trip_database.trips_table)
        
    def add_trip(self, trip_info={}):
        return trip.Trip.create_trip(trip_info)
        #return self.trip_db.create(trip_info)
        
    def remove_trip(self, id):
        self.get_trip(id).remove_trip()
        #return self.trip_db.remove(id)
        return id
    
    def get_trips(self):
        return self.trip_db.get_ids()
    
    def get_trip(self, id):
        if id not in self.get_trips():
            return None
        return trip.Trip(id)

    
            
            
         
    
    
    
        
    