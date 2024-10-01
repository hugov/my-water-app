import logging

from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def create_user(user):
        _user = user
        UserRepository.add(_user)
        return _user

    @staticmethod
    def get_user(id):
        return UserRepository.get_by_id(id)

    @staticmethod
    def list_user():
        return UserRepository.get_all()

    @staticmethod
    def delete_user(id):
        return UserRepository.delete_by_id(id)

