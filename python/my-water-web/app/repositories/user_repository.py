import logging
from app.models import User
from app import db

logger = logging.getLogger(__name__)

class UserRepository:

    @staticmethod
    def add(user):
        logger.debug("Adicionando uma usuário")
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        logger.debug(f"Consultando a usuário: {id}")
        return User.query.get(id)

    @staticmethod
    def get_all():
        logger.debug("Listando todas as usuários")
        return User.query.all()

    @staticmethod
    def delete_by_id(id):
        logger.debug(f"Excluindo a usuário: {id}")
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
