import datetime
import balance_calculator
    
class Trip:
    '''
    '''
    def __init__(self, id=''):
        self._persons = []
        self._payments = []
        self.info = {}
        self.info['id'] = id
        self.info['name'] = id
        self.info['description'] = ''
        self.info['date'] = datetime.date.today()
    
    def get_info(self):
        return self.info
    
    def add_person(self, person):
        '''
        add a new person.
        accept person dict or person id.
        - find existing person
        - if not found, create new and add
        - update contents
        '''
        if not isinstance(person, dict):
            person = {'id':person}
        
        id = person['id']
        entry = self.get_person(id)
        if not entry: 
            entry = {'id':id, 
                     'name':id, 
                     'weight':1 }
            self._persons.append(entry)
        entry.update(person)
        
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
        entry = None
        if payment.has_key('id'):
            entry = self.get_payment(payment['id'])
        if not entry:
            payment.pop('id', '') # ignore the input suggested id.
            entry = {'id':len(self._payments),
                       'creditor':"",
                       'amount':0,
                       'description':"",
                       'participants':[],
                       'date':datetime.date.today() }
            self._payments.append(entry)
        entry.update(payment)
        
    def remove_payment(self, index):
        if self.is_valid_payment_index(index): 
            del self._payments[index]

    def get_payment(self, index):
        if self.is_valid_payment_index(index):
            return self._payments[index]
        return None

    def is_valid_payment_index(self, index):    
        return index>=0 and index<len(self._payments)
     
    def get_payment_count(self):
        return len(self._payments)

