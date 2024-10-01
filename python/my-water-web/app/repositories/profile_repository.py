import logging
from app.models import Profile
from app import db

logger = logging.getLogger(__name__)

class ProfileRepository:

    @staticmethod
    def add(profile):
        logger.debug("Adicionando o perfil")
        db.session.add(profile)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        logger.debug(f"Consultando o perfil: {id}")
        return Profile.query.get(id)

    @staticmethod
    def get_all():
        logger.debug("Listando todos os perfis")
        return Profile.query.all()

    @staticmethod
    def delete_by_id(id):
        logger.debug(f"Excluindo o perfil: {id}")
        profile = Profile.query.get(id)
        if profile:
            db.session.delete(profile)
            db.session.commit()
