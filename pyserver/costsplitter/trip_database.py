import sqlalchemy
import datetime
import os.path
import os


if 'TRIP_DB' in os.environ:
    print 'Using database from environment variable TRIP_DB...' 
    db_name = os.environ['TRIP_DB']
else:
    print 'Using default in-memory database...'
    db_name = 'sqlite:///:memory:'
print 'Using database: ', db_name 
#print 'env', os.environ['TRIP_DB']


engine = sqlalchemy.create_engine(db_name, echo=False)


#>>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = sqlalchemy.MetaData()

trips_table = sqlalchemy.Table('trips', metadata,
     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
     sqlalchemy.Column('name', sqlalchemy.String),
     sqlalchemy.Column('description', sqlalchemy.String),
     sqlalchemy.Column('date', sqlalchemy.String)
      )
persons_table = sqlalchemy.Table('persons', metadata,
     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
     sqlalchemy.Column('name', sqlalchemy.String),
     sqlalchemy.Column('alias', sqlalchemy.String),
     sqlalchemy.Column('weight', sqlalchemy.Float),
     sqlalchemy.Column('trip', None, sqlalchemy.ForeignKey('trips.id'))
      )
payments_table = sqlalchemy.Table('payments', metadata,
     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
     sqlalchemy.Column('creditor', None, sqlalchemy.ForeignKey('persons.id')),
     sqlalchemy.Column('type', sqlalchemy.String),
     sqlalchemy.Column('amount', sqlalchemy.Float),
     sqlalchemy.Column('description', sqlalchemy.String),
     sqlalchemy.Column('currency', sqlalchemy.String),
     sqlalchemy.Column('rate', sqlalchemy.Float),
     #sqlalchemy.Column('participants', sqlalchemy.String),
     sqlalchemy.Column('date', sqlalchemy.String),
     sqlalchemy.Column('trip', None, sqlalchemy.ForeignKey('trips.id'))
      )
participants_table = sqlalchemy.Table('participants', metadata,
     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
     sqlalchemy.Column('payment', None, sqlalchemy.ForeignKey('payments.id')),
     sqlalchemy.Column('participant', None, sqlalchemy.ForeignKey('persons.id'))
      )


metadata.create_all(engine)

connection = engine.connect()


###############################################################################
class TripDB:
    '''
    CRUD database interface for the trip dictionary.
    '''
    def __init__(self, table):
        '''
        param: table: a sqlalchemy table
        param: default_content: a callable creating default content for the dict.
        '''
        self.connection = connection
        self.table = table
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
        c = self.connection
        result = c.execute(self.table.insert(), full_content)
        return result.inserted_primary_key[0]

    def remove(self, id):
        c = self.connection
        result = c.execute(self.table.delete().where(self.table.c.id==id))
        if result.rowcount == 0:
            return None
        return id

    def get_ids(self):
        c = self.connection
        result = c.execute(self.table.select())
        return [ one['id'] for one in result.fetchall() ]

    def update(self, content):
        c = self.connection
        id = content['id']
        result = c.execute(self.table.update().where(self.table.c.id==id), content)
    
    def get(self, id):
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.id==id))
        row = result.first()
        info = { key:row[key] for key in row.keys() }
        return info

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
    def __init__(self, table, trip_id):
        '''
        param: table: a sqlalchemy table
        param: default_content: a callable creating default content for the dict.
        '''
        self.connection = connection
        self.table = table
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
        full_content.update({'trip':self.trip_id})
        # insert into database and return new id       
        c = self.connection
        result = c.execute(self.table.insert(), full_content)
        return result.inserted_primary_key[0]

    def remove(self, id):
        c = self.connection
        result = c.execute(self.table.delete().where(self.table.c.id==id))
        if result.rowcount == 0:
            return None
        return id

    def get_ids(self):
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.trip==self.trip_id))
        return [ one['id'] for one in result.fetchall() ]

    def update(self, content):
        c = self.connection
        id = content['id']
        result = c.execute(self.table.update().where(self.table.c.id==id), content)
    
    def get(self, id):
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.id==id))
        row = result.first()
        if not row:
            return None
        info = { key:row[key] for key in self._public_person_table_keys() }
        return info

    def _public_person_table_keys(self):
        return ['id','name','alias','weight']

    def _create_default_content(self):
        return { 'name':'',
                 'alias':'',
                 'weight':1 }

###############################################################################
class PaymentDB:
    '''
    CRUD database interface for the payment dictionary.
    '''
    def __init__(self, table, trip_id):
        '''
        param: table: a sqlalchemy table
        param: default_content: a callable creating default content for the dict.
        '''
        self.connection = connection
        self.table = table
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
        full_content.update({'trip':self.trip_id})
        # insert into database and return new id       
        c = self.connection
        result = c.execute(self.table.insert(), full_content)
        id = result.inserted_primary_key[0]
        self._write_participants(id, full_content['participants'])
        return id

    def remove(self, id):
        c = self.connection
        result = c.execute(self.table.delete().where(self.table.c.id==id))
        c.execute(participants_table.delete().where(participants_table.c.payment==id))
        if result.rowcount == 0:
            return None
        return id

    def get_ids(self):  
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.trip==self.trip_id))
        return [ one['id'] for one in result.fetchall() ]

    def update(self, content):
        c = self.connection
        id = content['id']
        result = c.execute(self.table.update().where(self.table.c.id==id), content)
        if 'participants' in content:
            self._write_participants(id, content['participants'])
    
    def get(self, id):
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.id==id))
        row = result.first()
        if not row:
            return None
        info = { key:row[key] for key in self._public_payment_table_keys() }
        info['participants'] = self._read_participants(id)        
        return info

    def _read_participants(self, id):
        'read participants from the participants table'
        c = self.connection
        parts = c.execute(participants_table.select().where(participants_table.c.payment==id))
        participants = [part['participant'] for part in parts.fetchall()]
        return participants

    def _write_participants(self, id, participants):
        'sync participants table to the input participants list'
        c = self.connection
        old = self._read_participants(id)
        if old==participants:
            return
        # delete old
        if len(old)!=0:
            c.execute(participants_table.delete().where(participants_table.c.payment==id))
        # insert new
        if len(participants)!=0:
            for p in participants:
                c.execute(participants_table.insert(), {'payment':id, 'participant':p})
        
    def _public_payment_table_keys(self):
        return ['id','creditor','type','amount','description','currency','rate','date']

    def _create_default_content(self):
        return {   'creditor':0,
                   'type':'split',
                   'amount':0,
                   'description':"",
                   'rate':1.0,
                   'participants':[],
                   'date':datetime.date.today().isoformat() }
        