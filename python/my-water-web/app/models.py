import datetime

from . import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    price = db.Column(db.Integer)
    status = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'creation_date': self.creation_date.isoformat()  # Converte a data para string
        }