import costsplitter.trip
import costsplitter.trip_manager
import numpy.testing
import pprint
    
class TestTripManager:
    '''
    '''
    def test_add_one_trip(self):
        trips = costsplitter.trip_manager.TripManager()
        id = trips.add_trip({})
        assert int(id) is not None
        self.clear_trips()

    def test_add_two_trips_get_both(self):
        trips = costsplitter.trip_manager.TripManager()
        trip_input = [{'name':'n1',
                       'description':'desc2',
                       'date':'2016-05-07'},
                      {'name':'n2',
                       'description':'desc2',
                       'date':'2016-05-08'}
                      ]
        ids = []
        for input in trip_input:
            ids.append(trips.add_trip(input))
        assert ids == trips.get_trips()
        for input, id in zip(trip_input, ids):
            output = trips.get_trip(id)
            for key in input.keys():
                assert input[key] == output.get_info()[key]
        self.clear_trips()

    def test_get_nonexistent_trip(self):
        trips = costsplitter.trip_manager.TripManager()
        id = trips.add_trip({})
        assert trips.get_trip('no_trip') is None
        self.clear_trips()
    
    def clear_trips(self):
        trips = costsplitter.trip_manager.TripManager()
        ids = trips.get_trips()
        for id in ids:
            trips.remove_trip(id)
        assert len(trips.get_trips())==0


def temporary_trip(func):
    '''
    Decorator creating and removing a trip.
    The trip is available to func as self.trip.
    '''
    def func_wrapper(self):
        trips = costsplitter.trip_manager.TripManager()
        trip_id = trips.add_trip()
        self.trip = trips.get_trip(trip_id)
        try:
            return func(self)
        finally:
            trips.remove_trip(trip_id)
    return func_wrapper


class TestTrip:
    '''
    '''
    def init_data(self):
        '''
        create some nice test data
        '''
        #trips = costsplitter.trip_manager.TripManager()
        #self.trip = trips.get_trip(trips.add_trip())
        #self.trip = costsplitter.trip.Trip()
        self.persons = [{'name':'CA'},
                        {'name':'SAH'},
                        {'name':'HEA'}]
        self.payments = [{'creditor':1, #CA
                          'amount':300, 
                          'description':'Test payment of 300E.'},
                         {'creditor':2, #SAH
                          'amount':600, 
                          'description':'Test payment of 600E.'}]

    def fill_trip(self):
        '''
        insert the test data into the trip
        '''
        for person in self.persons:
            self.trip.add_person({'name':person['name']})
        for payment in self.payments:
            self.trip.add_payment(payment)
                    
    def _assert_payments_equal(self, a, b):
        '''
        find the subset c of b contained in a, 
        then check equality for a and c.
        '''
        c = {x:b[x] for x in a if x in b}
        assert a == c

    @temporary_trip
    def test_add_persons(self):
        self.init_data()        
        self.fill_trip()        
        #assert self.trip.get_persons() == self.persons
        for index, id in enumerate(self.trip.get_persons()):
            person = self.trip.get_person(id)
            assert self.persons[index]['name'] == person['name']

    @temporary_trip
    def test_remove_person(self):
        self.init_data()        
        self.fill_trip()        
        self.trip.remove_person(2)        
        assert self.trip.get_persons() == [1,3]
        
    @temporary_trip
    def test_add_payments(self):
        self.init_data()        
        self.fill_trip()
        assert len(self.payments) == len(self.trip.get_payments())
        for index, id in enumerate(self.trip.get_payments()):
            payment = self.trip.get_payment(id)
            self._assert_payments_equal(self.payments[index], payment)
                
    @temporary_trip
    def test_remove_payment(self):
        self.init_data()        
        self.fill_trip()
        self.trip.remove_payment(self.trip.get_payments()[0])
        assert len(self.payments)-1 == len(self.trip.get_payments())
        for index, id in enumerate(self.trip.get_payments()):
            self._assert_payments_equal(self.payments[index+1], self.trip.get_payment(id))
            
    @temporary_trip
    def test_add_payment_check_balance(self):
        self.init_data()        
        self.fill_trip()
        self.check_balance_for_person('CA',     0)
        self.check_balance_for_person('SAH',  300)
        self.check_balance_for_person('HEA', -300)
        
    @temporary_trip
    def test_add_payment_check_balance_weighted_person(self):
        self.init_data()  
        self.fill_trip()
        self.trip.update_person({'id':self.person_id('CA'), 
                                 'weight':7}) 
        # total weight of 9 for 900euro
        self.check_balance_for_person('CA',  -400)
        self.check_balance_for_person('SAH',  500)
        self.check_balance_for_person('HEA', -100)
                        
    @temporary_trip
    def test_add_payment_participant_subset(self):
        self.init_data()  
        self.fill_trip()
        self.trip.update_payment({'id':1, 
                                  'participants':[self.person_id('CA'), self.person_id('SAH')]})
        self.trip.update_payment({'id':2, 
                                  'participants':[self.person_id('CA'), self.person_id('SAH')]})
        self.check_balance_for_person('CA',  -150)
        self.check_balance_for_person('SAH',  150)
        self.check_balance_for_person('HEA',    0)

    @temporary_trip
    def test_add_debt_and_payment_check_balance(self):
        self.init_data()  
        self.fill_trip()
        self.trip.update_payment({'id':1, 
                                  'creditor':self.person_id('CA'), 
                                  'type':'debt',
                                  'amount':300, 
                                  'participants':[self.person_id('SAH')]})
        self.trip.update_payment({'id':2, 
                                  'creditor':self.person_id('SAH'), 
                                  'amount':600})
        self.check_balance_for_person('CA',   100)
        self.check_balance_for_person('SAH',  100)
        self.check_balance_for_person('HEA', -200)
                
    @temporary_trip
    def test_add_payment_foreign_currency_check_balance(self):
        self.init_data()        
        self.fill_trip()
        self.trip.update_payment({'id':1, 
                                  'rate':2, 
                                  'currency':'USD'})
        #pprint.pprint(self.trip._payments)
        # first payment: 300USD -> 600EUR
        # second payment: 600EUR
        self.check_balance_for_person('CA',   200)
        self.check_balance_for_person('SAH',  200)
        self.check_balance_for_person('HEA', -400)

    @temporary_trip
    def test_get_nonexistent_person(self):
        self.init_data()        
        self.fill_trip()
        assert self.trip.get_person('no_one') is None

    @temporary_trip
    def test_get_nonexistent_payment(self):
        self.init_data()        
        self.fill_trip()
        assert self.trip.get_payment('no_thing') is None

    def person_id(self, name):
        for id in self.trip.get_persons():
            person = self.trip.get_person(id)
            if person['name'] == name:
                return id

    def check_balance_for_person(self, person_name, expected_balance):
        for id in self.trip.get_persons():
            person = self.trip.get_person(id)
            if person['name'] == person_name:
                numpy.testing.assert_almost_equal(person['balance'],  expected_balance)
                break
