import costsplitter.trip
    
class TestTrip:
    '''
    '''
    def __init__(self):
        '''
        create some nice test data
        '''
        self.trip = costsplitter.trip.Trip()
        self.persons = ['CA', 'SAH', 'HEA']

    def fill_trip(self):
        '''
        insert the test data into the trip
        '''
        for person in self.persons:
            self.trip.add_person(person)
        
    def test_add_persons(self):
        self.fill_trip()
        
        assert self.trip.get_persons() == self.persons

    def test_remove_person(self):
        persons = ['CA', 'SAH', 'HEA']
        trip = costsplitter.trip.Trip()
        for person in persons:
            trip.add_person(person)
        trip.remove_person('SAH')
        
        assert trip.get_persons() == ['CA', 'HEA']
        
    def test_add_payments(self):
        trip = costsplitter.trip.Trip()
        persons = ['CA', 'SAH', 'HEA']
        for person in persons:
            trip.add_person(person)
        payments = [costsplitter.trip.Payment(person='CA', amount=300, description='Test payment of 300E.'),
                    costsplitter.trip.Payment(person='SAH', amount=600, description='Test payment of 600E.')]
        for payment in payments:
            trip.add_payment(payment)

        assert len(payments) == trip.get_payment_count()
        for i in range(len(payments)):
            assert payments[i] == trip.get_payment(i)
            
    def test_remove_payment(self):
        trip = costsplitter.trip.Trip()
        persons = ['CA', 'SAH', 'HEA']
        for person in persons:
            trip.add_person(person)
        payments = [costsplitter.trip.Payment(person='CA', amount=300, description='Test payment of 300E.'),
                    costsplitter.trip.Payment(person='SAH', amount=600, description='Test payment of 600E.')]
        for payment in payments:
            trip.add_payment(payment)
            
        trip.remove_payment(0)

        assert len(payments)-1 == trip.get_payment_count()
        for i in range(len(payments)-1):
            assert payments[i+1] == trip.get_payment(i)

#        payments.push_back(Payment("CA", 300, "Test payment of 300.", QStringList(), QDate(2013, 07, 29)));
#        payments.push_back(Payment("SAH", 600, "Test payment of 600.", QStringList(), QDate(2013, 07, 30)));
        
