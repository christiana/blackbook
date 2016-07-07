import datetime

def foo():
    print "hello trip"
    
class Payment:
    '''
    '''
    def __init__(self, person="", amount="", 
                    description="", 
                    participants=[], 
                    date=datetime.date.today()):
        self.person = person
        self.amount = amount
        self.description = description
        self.participants = participants
        self.date = date
    

    
    
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
    
    def add_person(self, name):
        self._persons.append(name)
        
    def remove_person(self, name):
        if name in self._persons:
            self._persons.remove(name)
    
    def get_persons(self):
        return self._persons
    
    def add_payment(self, payment):
        self._payments.append(payment)
        
    def remove_payment(self, index):
        del self._payments[index]

    def get_payment(self, index):
        return self._payments[index]
    
    def get_payment_count(self):
        return len(self._payments)
        
    def add_payment_(self, person, amount, 
                    description=Payment().description, 
                    participants=Payment().participants, 
                    date=Payment().date):
        payment = Payment()
        payment.person = person
        payment.amount = amount
        payment.description = description
        payment.participants = participants
        payment.date = date
        self.add_payment(payment)
#        payments.push_back(Payment("CA", 300, "Test payment of 300.", QStringList(), QDate(2013, 07, 29)));
