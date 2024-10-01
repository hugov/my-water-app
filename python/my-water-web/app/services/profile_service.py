import logging

from app.repositories.profile_repository import ProfileRepository

logger = logging.getLogger(__name__)

class ProfileService:

    @staticmethod
    def create_profile(profile):
        _profile = profile
        ProfileRepository.add(_profile)
        return _profile

    @staticmethod
    def get_profile(id):
        return ProfileRepository.get_by_id(id)

    @staticmethod
    def list_profile():
        return ProfileRepository.get_all()

    @staticmethod
    def delete_profile(id):
        return ProfileRepository.delete_by_id(id)

