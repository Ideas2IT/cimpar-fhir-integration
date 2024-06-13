from fastapi import APIRouter
import logging

from models.auth_validation import UserModel, TokenModel
from controller.auth_controller import AuthClient


router = APIRouter()
logger = logging.getLogger("log")


@router.post('/sign_up')
async def create_account(user_plan: UserModel):
    logger.info("Request Payload: %s" % user_plan)
    response = AuthClient.create(user_plan)
    logger.info("Response: %s" % response)
    return response


@router.post('/login')
async def create_token(token: TokenModel):
    logger.info("Request Payload: %s" % token)
    response = AuthClient.create_token(token)
    logger.info("Response: %s" % response)
    return response
