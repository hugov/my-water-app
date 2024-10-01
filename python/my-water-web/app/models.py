import datetime

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    document = db.Column(db.String(50), unique=True, nullable=False)  # CPF ou CNPJ, dependendo do caso
    phone = db.Column(db.String(20))  # Número de telefone
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Armazene a senha de forma segura (hash)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    status = db.Column(db.Integer, nullable=False, default=1)  # Ex: 1 para ativo, 0 para inativo

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
            'creation_date': self.creation_date.isoformat(),  # Converte a data para string
            'status': self.status
        }

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

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))  # URL ou caminho da imagem
    status = db.Column(db.Integer, nullable=False, default=1)  # Ex: 1 para ativo, 0 para inativo
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
            'creation_date': self.creation_date.isoformat()  # Converte a data para string
        }