import trip_database
db = trip_database.db


###############################################################################
class ModelCRUD:
    '''
    CRUD(create-update-get-delete) database interface for the given flask-sqlalchemy model.
    '''
    def __init__(self, model):
        self.Model = model
        
    def create(self, content):
        if not isinstance(content, dict):
            raise Exception('expected dict')
        if 'id' in content:
            raise Exception('id not allowed as input to entry creation')
        entry = self.Model(content)
        db.session.add(entry)
        db.session.commit()
        return entry.id

    def remove(self, id):
        entry = self.Model.query.get(id)
        if not entry:
            return None
        db.session.delete(entry)
        db.session.commit()
        return entry.id

    def update(self, content):
        entry = self.Model.query.get(content['id'])
        if not entry:
            return None
        entry.update(content)
        db.session.commit()
            
    def get(self, id):
        entry = self.Model.query.get(id)
        if not entry:
            return None
        return entry.get_public_values()
