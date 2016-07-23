import datetime
import balance_calculator
import trip_database
import pprint
import werkzeug.exceptions
#from werkzeug.exceptions import BadRequest
#raise BadRequest('My custom message')
    
    
class Trip:
    '''
    Wraps one existing trip in the database.
    The database trip itself is created/destroyed by the TripManager
    '''
    @staticmethod
    def create_trip(trip_info):
        trip = Trip()
        trip._validate_info(trip_info)
        id = trip.trip_db.create(trip_info)
        return id
    
    def remove_trip(self):
        for payment in self.get_payments():
            self.remove_payment(payment)
        for person in self.get_persons():
            self.remove_person(person)
        self.trip_db.remove(self.id)
        self.id = None
    
    def __init__(self, id=None):
        self.id = id
        self.trip_db = trip_database.TripDB(table=trip_database.trips_table)
        self.payment_db = trip_database.PaymentDB(table=trip_database.payments_table, trip_id=id)
        self.person_db = trip_database.PersonDB(table=trip_database.persons_table, trip_id=id)

    def get_info(self):
        return self.trip_db.get(self.id)
    
    def set_info(self, info):
        info = info.copy()
        info['id'] = self.id
        self._validate_info(info)
        self.trip_db.update(info)

    def _validate_datestring(self, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            bad = werkzeug.exceptions.BadRequest()
            bad.data = {'message' : 'Non-ISO date: %s'%date, 'exception' : str(e)}
            raise bad

    def _validate_info(self, info):
        if 'date' in info:
            self._validate_datestring(info['date']);

    def _validate_payment(self, payment):
        if 'date' in payment:
            self._validate_datestring(payment['date']);
    
    def add_person(self, content):
        content = content.copy();
        content['trip_id'] = self.id
        return self.person_db.create(content)

    def update_person(self, content):
        return self.person_db.update(content)
        
    def remove_person(self, id):
        return self.person_db.remove(id)
    
    def get_persons(self):
        return self.person_db.get_ids()

    def get_person(self, id):
        person = self.person_db.get(id)
        if not person:
            return None
        persons = [self.person_db.get(id) for id in self.get_persons() ]
        payments = [self.payment_db.get(id) for id in self.get_payments() ]        
        calculator = balance_calculator.BalanceCalculator(persons=persons, payments=payments)
        person['balance'] = calculator.calculate_balance_for_person(person)
        return person
    
    def add_payment(self, content):
        content = content.copy();
        content['trip_id'] = self.id
        self._validate_payment(content)
        return self.payment_db.create(content)
        
    def update_payment(self, content):
        self._validate_payment(content)
        return self.payment_db.update(content)

    def remove_payment(self, id):
        return self.payment_db.remove(id)

    def get_payment(self, id):
        return self.payment_db.get(id)

    def get_payments(self):
        return self.payment_db.get_ids()
