import logging

from models.auth_validation import UserModel, TokenModel
from controller.auth_controller import AuthClient

logger = logging.getLogger("log")


class AuthService:
    @staticmethod
    def create_user(user: UserModel):
        return AuthClient.create(user)

    @staticmethod
    def create_token(token: TokenModel):
        return AuthClient.create_token(token)

