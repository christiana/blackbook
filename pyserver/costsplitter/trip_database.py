import sqlalchemy
import flask_sqlalchemy
import datetime
import os.path
import os

import trip_app
app = trip_app.app


if 'TRIP_DB' in os.environ:
    print 'Using database from environment variable TRIP_DB...' 
    db_name = os.environ['TRIP_DB']
else:
    print 'Using default in-memory database...'
    db_name = 'sqlite:///:memory:'
print 'Using database: ', db_name 
#print 'env', os.environ['TRIP_DB']

trip_app.app.config['SQLALCHEMY_DATABASE_URI'] = db_name
db = flask_sqlalchemy.SQLAlchemy(app)


class Trip(db.Model):
    ''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String)
    # implicit: person ref to [Person]
    # implicit: payments ref to [Payment]
    def __init__(self, content):
        self.__dict__.update(content)
    def update(self, content):
        
        for (key, value) in content.items():
            if not hasattr(self, key):
                continue
            if key=='id':
                continue
            assert hasattr(self, key)
            setattr(self, key, value)
        pass

class Person(db.Model):
    ''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    alias = db.Column(db.String)
    weight = db.Column(db.Float)
    trip_id = db.Column(None, db.ForeignKey('trip.id'))
    trip = db.relationship('Trip', 
                           backref=db.backref('persons', 
                                              lazy='dynamic',
                                              cascade="delete, delete-orphan"))     
                      
    def __init__(self, content):
        self.update(content)
    def update(self, content):
        for (key, value) in content.items():
            if not hasattr(self, key):
                continue
            if key=='id':
                continue
            assert hasattr(self, key), 'did not find key %s in object %s' % (key, self.__class__.__name__)
            setattr(self, key, value)
        pass

class Payment(db.Model):
    ''
    id = db.Column(db.Integer, primary_key=True)
    creditor = db.Column(None, db.ForeignKey('person.id'))
#    creditor_id = db.Column(None, db.ForeignKey('person.id'))
#    creditor = db.relationship('Person')     
    type = db.Column(db.String)
    amount = db.Column(db.Float)
    description = db.Column(db.String)
    currency = db.Column(db.String)
    rate = db.Column(db.Float)
    date = db.Column(db.String)
    trip_id = db.Column(None, db.ForeignKey('trip.id'))
    trip = db.relationship('Trip', 
                           backref=db.backref('payments', 
                                              lazy='dynamic',
                                              cascade="delete, delete-orphan"))     
    # implicit: participants ref to [Participant]

    def __init__(self, content):
        self.update(content)
    def update(self, content):
        for (key, value) in content.items():
            if not hasattr(self, key):
                continue
            if key=='participants':
                self.participants = [Participant({'person_id':p}) for p in content['participants']]
            else:
                setattr(self, key, value)
          
class Participant(db.Model):
    ''
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(None, db.ForeignKey('payment.id'))
    payment = db.relationship('Payment', 
                              backref=db.backref('participants', 
                                                 lazy='dynamic', 
                                                 cascade="all, delete, delete-orphan"))     
    person_id = db.Column(None, db.ForeignKey('person.id'))
    person = db.relationship('Person')     

    def __init__(self, content):
        self.__dict__.update(content)

    def __repr__(self):
        return '<Participant person=%s>' % str(self.person_id)

db.create_all()
#metadata.create_all(engine)

#connection = engine.connect()


###############################################################################
class TripDB:
    '''
    CRUD database interface for the trip dictionary.
    '''
    def __init__(self):
        '''
        '''
        pass
    
    def create(self, content):        
        if not isinstance(content, dict):
            raise Exception('expected dict')
        if 'id' in content:
            raise Exception('id not allowed as input to entry creation')
        # start out with the default dict, then fill in the input dict        
        full_content = self._create_default_content()
        full_content.update(content) 
        
        # insert into database and return new id       
        trip = Trip(full_content)
        db.session.add(trip)
        db.session.commit()
        return trip.id

    def remove(self, id):
        entry = Trip.query.get(id)
        if not entry:
            return None
        db.session.delete(entry)
        db.session.commit()
        return entry.id

    def get_ids(self):
        return [trip.id for trip in Trip.query.all()]
        
    def update(self, content):
        entry = Trip.query.get(content['id'])
        if not entry:
            return None
        entry.update(content)
        db.session.commit()
    
    def get(self, id):
        entry = Trip.query.get(id)
        if not entry:
            return None
        return { key:entry.__dict__[key] for key in self._public_table_keys() }

    def _public_table_keys(self):
        return ['id','description','date','name']

    def _create_default_content(self):
        date = datetime.date.today().isoformat()
        return {  'description':'',
                  'date':date,
                  'name':'Trip_%s' % date } 

###############################################################################
class PersonDB:
    '''
    CRUD database interface for the person dictionary.
    '''
    def __init__(self, trip_id):
        '''
        '''
        self.Table = Person
        self.trip_id = trip_id
        pass
    
    def create(self, content):        
        if not isinstance(content, dict):
            raise Exception('expected dict')
        if 'id' in content:
            raise Exception('id not allowed as input to entry creation')
        # start out with the default dict, then fill in the input dict        
        full_content = self._create_default_content()
        full_content.update(content) 
#        full_content.update({'trip':self.trip_id})
        
        # insert into database and return new id       
        entry = self.Table(full_content)
        db.session.add(entry)
        db.session.commit()
        return entry.id

    def remove(self, id):
        entry = self.Table.query.get(id)
        if not entry:
            return None
        db.session.delete(entry)
        db.session.commit()
        return entry.id

    def get_ids(self):
        return [entry.id for entry in self.Table.query.filter_by(trip_id=self.trip_id)]
        
    def update(self, content):
        entry = self.Table.query.get(content['id'])
        if not entry:
            return None
        entry.update(content)
        db.session.commit()
    
    def get(self, id):
        entry = self.Table.query.get(id)
        if not entry:
            return None
        return { key:entry.__dict__[key] for key in self._public_table_keys() }

    def _public_table_keys(self):
        return ['id','name','alias','weight']

    def _create_default_content(self):
        return { 'name':'',
                 'alias':'',
                 'weight':1,
                 'trip_id':self.trip_id
                 }

###############################################################################
class PaymentDB:
    '''
    CRUD database interface for the payment dictionary.
    '''
    def __init__(self, trip_id):
        self.Table = Payment
        self.trip_id = trip_id
        
    def create(self, content):
        if not isinstance(content, dict):
            raise Exception('expected dict')
        if 'id' in content:
            raise Exception('id not allowed as input to entry creation')
        # start out with the default dict, then fill in the input dict
        full_content = self._create_default_content()
        full_content.update(content) 
        # insert into database and return new id       
        entry = self.Table(full_content)
        db.session.add(entry)
        db.session.commit()
        return entry.id

    def remove(self, id):
        entry = self.Table.query.get(id)
        if not entry:
            return None
        db.session.delete(entry)
        db.session.commit()
        return entry.id

    def get_ids(self):  
        return [entry.id for entry in self.Table.query.filter_by(trip_id=self.trip_id)]

    def update(self, content):
        entry = self.Table.query.get(content['id'])
        if not entry:
            return None
        entry.update(content)
        db.session.commit()
            
    def get(self, id):
        entry = self.Table.query.get(id)
        if not entry:
            return None
        retval =  { key:entry.__dict__[key] for key in self._public_table_keys() }
        retval['participants'] = [p.person_id for p in entry.participants]
        return retval
        
    def _public_table_keys(self):
        return ['id','creditor','type','amount','description','currency','rate','date']

    def _create_default_content(self):
        return {   'creditor':0,
                   'type':'split',
                   'amount':0,
                   'description':"",
                   'rate':1.0,
                   'currency':"",
                   'participants':[],
                   'date':datetime.date.today().isoformat(), 
                   'trip_id':self.trip_id
                   }
        