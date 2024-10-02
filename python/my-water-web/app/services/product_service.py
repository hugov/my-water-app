import logging

from app.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductService:

    @staticmethod
    def create_product(product):
        _product = product
        ProductRepository.add(_product)
        return _product

    @staticmethod
    def get_product(id):
        return ProductRepository.get_by_id(id)

    @staticmethod
    def list_product():
        return ProductRepository.get_all()

    @staticmethod
    def list_product_by_category(category_id):
        return ProductRepository.list_product_by_category(category_id)

    @staticmethod
    def delete_product(id):
        return ProductRepository.delete_by_id(id)
