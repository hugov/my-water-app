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