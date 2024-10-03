import logging

from app.repositories.category_repository import CategoryRepository

logger = logging.getLogger(__name__)

class CategoryService:

    @staticmethod
    def create_category(category):
        _category = category
        CategoryRepository.add(_category)
        return _category

    @staticmethod
    def get_category(id):
        return CategoryRepository.get_by_id(id)

    @staticmethod
    def list_category():
        return CategoryRepository.get_all()

    @staticmethod
    def delete_category(id):
        return CategoryRepository.delete_by_id(id)

    @staticmethod
    def get_image_name(filename):
        return CategoryRepository.get_image_name(filename)

