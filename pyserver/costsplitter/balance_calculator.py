
class BalanceCalculator:
    '''
    '''
    def __init__(self, payments, persons):
        self.payments = payments
        self.persons = persons
        
    def calculate_balance_for_person(self, person):
        sum = 0.0
        for payment in self.payments:
            sum += self.calculate_balance_for_person_per_payment(person, payment)
        return sum

    def calculate_balance_for_person_per_payment(self, person, payment):
        retval = 0.0
        if person['id'] == payment['creditor']:
            retval += payment['amount']
        fraction = self.get_fraction_for_person(person, payment)
        retval -= fraction * payment['amount'] 
        return retval
    
    def get_fraction_for_person(self, person, payment):
        participants = self.get_participants_for_payment(payment)
        totalweight = 0.0
        weight = 0.0
        for p in self.persons:
            if p['id'] in participants:
                totalweight += p['weight']
            if p['id'] == person['id']:
                weight = p['weight']
        return weight/totalweight        
        
    def get_participants_for_payment(self, payment):
        if len(payment['participants'])==0:
            return [p['id'] for p in self.persons]
        else:
            return payment['participants']


