import logging

from app.models import Product
from app import db

logger = logging.getLogger(__name__)

class ProductRepository:

    @staticmethod
    def add(product):
        logger.debug("Adicionando um produto")
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        logger.debug(f"Consultando o produto: {id}")
        return Product.query.get(id)

    @staticmethod
    def get_all():
        logger.debug("Listando todos os produtos")
        return Product.query.all()

    @staticmethod
    def list_product_by_category(category_id):
        logger.debug("Listando os produtos pela categoria")
        return Product.query.filter_by(category_id=category_id).all()

    @staticmethod
    def delete_by_id(id):
        logger.debug(f"Excluindo o produto: {id}")

        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()

