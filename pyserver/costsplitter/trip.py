import datetime
import balance_calculator
import trip_database
    
class Trip:
    '''
    '''
    def __init__(self, id=None):
        self.id = id
        self.table_handler = trip_database.TableHandler(table=trip_database.trips_table, 
                                                        default_content=Trip.create_default_info)
        self._persons = []
        self._payments = []
        #self.info = {}
        #self.info['description'] = ''
        #self.info['date'] = datetime.date.today().isoformat()
        #self.info['name'] = 'Trip_%s' % self.info['date'] 
        #self.info.update(info)
    
    @staticmethod
    def create_default_info():
        retval = {}
        retval['description'] = ''
        retval['date'] = datetime.date.today().isoformat()
        retval['name'] = 'Trip_%s' % retval['date'] 
        return retval

    def get_info(self):
        return self.table_handler.get(self.id)
        #return self.info
    
    def set_info(self, info):
        self.table_handler.update(self.id)
        #self.info.update(info)
    
    def add_person(self, person):
        '''
        add a new person.
        accept person dict or person id.
        - find existing person
        - if not found, create new and add
        - update contents
        '''
        if not isinstance(person, dict):
            assert isinstance(person, basestring)
            person = {'id':person}
        if 'id' not in person:
            person['id'] = self._generate_unique_person_id()
        
        id = person['id']
        entry = self.get_person(id)
        if not entry: 
            entry = {'id':id, 
                     'name':id, 
                     'weight':1 }
            self._persons.append(entry)
        entry.update(person)
        return id
        
    def remove_person(self, id):
        self._persons.remove(self.get_person(id))
    
    def get_persons(self):
        return [person['id'] for person in self._persons]

    def _update_derived_values(self):
        #print '_update_derived_values:'
        #print 'persons:', self._persons
        #print 'payments:', self._payments
        calculator = balance_calculator.BalanceCalculator(persons=self._persons, payments=self._payments)
        for p in self._persons:
            p['balance'] = calculator.calculate_balance_for_person(p)

    def get_person(self, id):
        self._update_derived_values()
        for current in self._persons:
            if current['id'] == id:
                return current
        return None
    
    def add_payment(self, payment):
        if not isinstance(payment, dict):
            assert isinstance(payment, basestring)
            payment = {'id':payment}
        if 'id' not in payment:
            payment['id'] = self._generate_unique_payment_id()
        
        id = payment['id']
        entry = self.get_payment(id)
        
        
#        entry = None
#        if payment.has_key('id'):
#            entry = self.get_payment(payment['id'])
        if not entry:
            #payment.pop('id', '') # ignore the input suggested id.
            entry = {'id':len(self._payments),
                       'creditor':"",
                       'type':'split',
                       'amount':0,
                       'description':"",
                       'rate':1.0,
                       'participants':[],
                       'date':datetime.date.today().isoformat() }
            self._payments.append(entry)
        entry.update(payment)
        return id
        
    def remove_payment(self, id):
        self._payments.remove(self.get_payment(id))
#        if self.is_valid_payment_index(index): 
#            del self._payments[index]

    def get_payment(self, id):
        for current in self._payments:
            if current['id'] == id:
                return current
        return None
#        if self.is_valid_payment_index(index):
#            return self._payments[index]
#        return None

    def get_payments(self):
        return [entry['id'] for entry in self._payments]

#    def is_valid_payment_index(self, index):    
#        return index>=0 and index<len(self._payments)
     
#    def get_payment_count(self):
#        return len(self._payments)
    
    def _generate_unique_person_id(self):
        i = 0
        while True:
            uid = 'person%s' % i
            if not self.get_person(uid):
                return uid
            i = i+1

    def _generate_unique_payment_id(self):
        i = 0
        while True:
            uid = 'payment%s' % i
            if not self.get_payment(uid):
                return uid
            i = i+1

