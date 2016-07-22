import datetime
import trip
import trip_database
    
    
class TripManager:
    '''
    '''
    def __init__(self):
        self.table_handler = trip_database.TableHandler(table=trip_database.trips_table, 
                                                        default_content=trip.Trip.create_default_info)
        
    def add_trip(self, trip_info={}):
        return self.table_handler.create(trip_info)
#        if not isinstance(trip_info, dict):
#            raise Exception('expected dict')
#        if 'id' in trip_info:
#            raise Exception('id not allowed as input to entry creation')
#        entry = trip.Trip()
#        entry.set_info(trip_info)
#        db = trip_database
#        result = db.connection.execute(db.trips_table.insert(), entry.get_info())
#        #print "result.inserted_primary_key ", result.inserted_primary_key        
#        return result.inserted_primary_key[0]
        
    def remove_trip(self, id):
        return self.table_handler.remove(id)
#        db = trip_database
#        result = db.connection.execute(db.trips_table.delete().where(db.trips_table.c.id==id))
        #self.trips.remove(self.get_trip(name))
    
    def get_trips(self):
        return self.table_handler.get_ids()
#        db = trip_database
#        result = db.connection.execute(db.trips_table.select())
        #for row in result:
        #    print "--trip:", row
        #print "get_trips ", len(self.trips) 
        #return [trip.get_info()['id'] for trip in self.trips]
#        return [ one['id'] for one in result.fetchall() ]
    
    def get_trip(self, id):
        return trip.Trip(id)
#        self.table_handler.get(id)
#        db = trip_database
#        result = db.connection.execute(db.trips_table.select().where(db.trips_table.c.id==id))
#        row = result.first()
#        info = { key:row[key] for key in row.keys() }
#        return trip.Trip(info)

    
            
            
         
    
    
    
        
    