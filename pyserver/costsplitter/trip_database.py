import sqlalchemy
#from sqlalchemy import create_engine

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)


#>>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = sqlalchemy.MetaData()

trips_table = sqlalchemy.Table('trips', metadata,
     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
     sqlalchemy.Column('name', sqlalchemy.String),
     sqlalchemy.Column('description', sqlalchemy.String),
     sqlalchemy.Column('date', sqlalchemy.String)
      )

metadata.create_all(engine)

connection = engine.connect()


class TableHandler:
    '''
    Convenience wrapper for a CRUD list-of-dict
    '''
    def __init__(self, table, default_content):
        '''
        param: table: a sqlalchemy table
        param: default_content: a callable creating default content for the dict.
        '''
        self.connection = connection
        self.table = table
        self.default_content = default_content
        pass
    
    def create(self, content):
        if not isinstance(content, dict):
            raise Exception('expected dict')
        if 'id' in content:
            raise Exception('id not allowed as input to entry creation')
        # start out with the default dict, then fill in the input dict        
        full_content = self.default_content()
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

    def update(self, id, content):
        c = self.connection
        result = c.execute(self.table.update().where(self.table.c.id==id), content)
    
    def get(self, id):
        c = self.connection
        result = c.execute(self.table.select().where(self.table.c.id==id))
        row = result.first()
        info = { key:row[key] for key in row.keys() }
        return info




