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


###############################################################################
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

    def get_public_values(self):
        return { key:self.__dict__[key] for key in self._public_table_keys() }

    def _public_table_keys(self):
        return ['id','description','date','name']

###############################################################################
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
        
    def get_public_values(self):
        return { key:self.__dict__[key] for key in self._public_table_keys() }

    def _public_table_keys(self):
        return ['id','name','alias','weight']

###############################################################################
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

    def get_public_values(self):
        retval =  { key:self.__dict__[key] for key in self._public_table_keys() }
        retval['participants'] = [p.person_id for p in self.participants]
        return retval
        
    def _public_table_keys(self):
        return ['id','creditor','type','amount','description','currency','rate','date']
          
###############################################################################
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

###############################################################################
db.create_all()
###############################################################################



        