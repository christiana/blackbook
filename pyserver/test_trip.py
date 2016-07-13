import costsplitter.trip
import numpy.testing
import pprint
    
class TestTrip:
    '''
    '''
    def init_data(self):
        '''
        create some nice test data
        '''
        self.trip = costsplitter.trip.Trip()
        self.persons = ['CA', 'SAH', 'HEA']
        self.payments = [{'id':'0', 
                          'creditor':'CA', 
                          'amount':300, 
                          'description':'Test payment of 300E.'},
                         {'id':'1', 
                          'creditor':'SAH', 
                          'amount':600, 
                          'description':'Test payment of 600E.'}]

    def fill_trip(self):
        '''
        insert the test data into the trip
        '''
        for person in self.persons:
            self.trip.add_person(person)
        for payment in self.payments:
            self.trip.add_payment(payment)
        
    def _assert_payments_equal(self, a, b):
        '''
        find the subset c of b contained in a, 
        then check equality for a and c.
        '''
        c = {x:b[x] for x in a if x in b}
        assert a == c

    def test_add_persons(self):
        self.init_data()        
        self.fill_trip()        
        assert self.trip.get_persons() == self.persons

    def test_remove_person(self):
        self.init_data()        
        self.fill_trip()        
        self.trip.remove_person('SAH')        
        assert self.trip.get_persons() == ['CA', 'HEA']
        
    def test_add_payments(self):
        self.init_data()        
        self.fill_trip()
        assert len(self.payments) == len(self.trip.get_payments())
        for index, id in enumerate(self.trip.get_payments()):
            self._assert_payments_equal(self.payments[index], self.trip.get_payment(id))
                
    def test_remove_payment(self):
        self.init_data()        
        self.fill_trip()
        self.trip.remove_payment(self.trip.get_payments()[0])
        assert len(self.payments)-1 == len(self.trip.get_payments())
        for index, id in enumerate(self.trip.get_payments()):
#        for i in range(len(self.trip.payments)-1):
            self._assert_payments_equal(self.payments[index+1], self.trip.get_payment(id))
            #assert self.payments[i+1] == self.trip.get_payment(i)
            
    def test_add_payment_check_balance(self):
        self.init_data()        
        self.fill_trip()
        numpy.testing.assert_almost_equal(self.trip.get_person('CA')['balance'],     0)
        numpy.testing.assert_almost_equal(self.trip.get_person('SAH')['balance'],  300)
        numpy.testing.assert_almost_equal(self.trip.get_person('HEA')['balance'], -300)
        
    def test_add_payment_check_balance_weighted_person(self):
        self.init_data()  
        self.fill_trip()
        self.trip.add_person({'id':'CA', 'weight':7})
        # total weight of 9 for 900euro
        numpy.testing.assert_almost_equal(self.trip.get_person('CA')['balance'],  -400)
        numpy.testing.assert_almost_equal(self.trip.get_person('SAH')['balance'],  500)
        numpy.testing.assert_almost_equal(self.trip.get_person('HEA')['balance'], -100)
        
    def test_add_payment_participant_subset(self):
        self.init_data()  
        self.fill_trip()
        self.trip.add_payment({'id':'0', 'participants':['CA','SAH']})
        self.trip.add_payment({'id':'1', 'participants':['CA','SAH']})
        numpy.testing.assert_almost_equal(self.trip.get_person('CA')['balance'], -150)
        numpy.testing.assert_almost_equal(self.trip.get_person('SAH')['balance'], 150)
        numpy.testing.assert_almost_equal(self.trip.get_person('HEA')['balance'],   0)

    def test_add_debt_and_payment_check_balance(self):
        self.init_data()  
        self.payments = [{'creditor':'CA', 
                          'type':'debt',
                          'amount':300, 
                          'participants':['SAH'],
                          'description':'Test payment of 300E.'},
                         {'creditor':'SAH', 
                          'amount':600, 
                          'description':'Test payment of 600E.'}]
        self.fill_trip()
        numpy.testing.assert_almost_equal(self.trip.get_person('CA')['balance'],   100)
        numpy.testing.assert_almost_equal(self.trip.get_person('SAH')['balance'],  100)
        numpy.testing.assert_almost_equal(self.trip.get_person('HEA')['balance'], -200)
        
        
    def test_add_payment_foreign_currency_check_balance(self):
        self.init_data()        
        self.fill_trip()
        self.trip.add_payment({'id':'0', 'rate':2, 'currency':'USD'})
        #pprint.pprint(self.trip._payments)
        # first payment: 300USD -> 600EUR
        # second payment: 600EUR
        numpy.testing.assert_almost_equal(self.trip.get_person('CA')['balance'],   200)
        numpy.testing.assert_almost_equal(self.trip.get_person('SAH')['balance'],  200)
        numpy.testing.assert_almost_equal(self.trip.get_person('HEA')['balance'], -400)
