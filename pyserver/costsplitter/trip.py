import datetime
import balance_calculator
import trip_database
import trip_model_crud
import pprint
import werkzeug.exceptions    
    
class Trip:
    '''
    Wraps one existing trip in the database.
    The database trip itself is created/destroyed by the TripManager
    '''
    @staticmethod
    def create_trip(trip_info):
        trip = Trip()
        c = trip._create_default_trip_content()
        c.update(trip_info)
        trip._validate_info(c)
        id = trip.trip_db.create(c)
        return id
    
    def remove_trip(self):
        self.trip_db.remove(self.id)
        self.id = None
    
    def __init__(self, id=None):
        self.id = id
        self.trip_db = trip_model_crud.ModelCRUD(trip_database.Trip)
        self.payment_db = trip_model_crud.ModelCRUD(trip_database.Payment)
        self.person_db = trip_model_crud.ModelCRUD(trip_database.Person)

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
        if 'creditor' in payment:
            if payment['creditor'] not in self.get_persons():
                raise werkzeug.exceptions.BadRequest('creditor %s does not exist.'%payment['creditor'])
        if 'participants' in payment:
            persons = self.get_persons()
            for p in payment['participants']:
                if p not in persons:
                    raise werkzeug.exceptions.BadRequest('participant %s does not exist.'%p)
    
    def add_person(self, content):
        c = self._create_default_person_content()
        c.update(content)
        return self.person_db.create(c)

    def update_person(self, content):
        return self.person_db.update(content)
        
    def remove_person(self, id):
        return self.person_db.remove(id)
    
    def get_persons(self):
        return [entry.id for entry in trip_database.Person.query.filter_by(trip_id=self.id)]

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
        c = self._create_default_payment_content()
        c.update(content) 
        self._validate_payment(content) # hack: the default creditor is invalid, thus validate only input for now.
        return self.payment_db.create(c)
        
    def update_payment(self, content):
        self._validate_payment(content)
        return self.payment_db.update(content)

    def remove_payment(self, id):
        return self.payment_db.remove(id)

    def get_payment(self, id):
        return self.payment_db.get(id)

    def get_payments(self):
        return [entry.id for entry in trip_database.Payment.query.filter_by(trip_id=self.id)]
        
        
    def _create_default_trip_content(self):
        date = datetime.date.today().isoformat()
        return {  'description':'',
                  'date':date,
                  'name':'Trip_%s' % date } 

    def _create_default_payment_content(self):
        return {   'creditor':0,
                   'type':'split',
                   'amount':0,
                   'description':"",
                   'rate':1.0,
                   'currency':"",
                   'participants':[],
                   'date':datetime.date.today().isoformat(), 
                   'trip_id':self.id
                   }

    def _create_default_person_content(self):
        return { 'name':'',
                 'alias':'',
                 'weight':1,
                 'trip_id':self.id
                 }
