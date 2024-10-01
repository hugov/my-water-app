import logging
from app.models import Category
from app import db

logger = logging.getLogger(__name__)

class CategoryRepository:

    @staticmethod
    def add(category):
        logger.debug("Adicionando uma categoria")
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        logger.debug(f"Consultando a categoria: {id}")
        return Category.query.get(id)

    @staticmethod
    def get_all():
        logger.debug("Listando todas as categorias")
        return Category.query.all()

    @staticmethod
    def delete_by_id(id):
        logger.debug(f"Excluindo a categoria: {id}")
        category = Category.query.get(id)
        if category:
            db.session.delete(category)
            db.session.commit()
