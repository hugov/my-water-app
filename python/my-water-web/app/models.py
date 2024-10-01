import datetime

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    document = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    status = db.Column(db.Integer, nullable=False, default=1)
    def __repr__(self):
        return '<User id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'document': self.document,
            'phone': self.phone,
            'username': self.username,
            'creation_date': self.creation_date,
            'status': self.status
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    price = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, default=1)
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
            'creation_date': self.creation_date
        }

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))  # URL ou caminho da imagem
    status = db.Column(db.Integer, nullable=False, default=1)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return '<Category id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'status': self.status,
            'creation_date': self.creation_date
        }

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255))
    allows_create = db.Column(db.Integer)
    allows_retrieve = db.Column(db.Integer)
    allows_updated = db.Column(db.Integer)
    allows_delete = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, default=1)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return '<Category id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'allows_create': self.allows_create,
            'allows_retrieve': self.allows_retrieve,
            'allows_updated': self.allows_updated,
            'allows_delete': self.allows_delete,
            'status': self.status,
            'creation_date': self.creation_date
        }