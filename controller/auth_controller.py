from fastapi import Response, status, HTTPException
import logging
import traceback
from aidbox.base import API

from models.auth_validation import (
    UserModel, TokenModel,
    User, AccessPolicy, CimparRole, CimparPermission
)
from services.aidbox_service import AidboxApi
from utils.common_utils import generate_permission_id

logger = logging.getLogger("log")


class AuthClient:
    @staticmethod
    def create(user: UserModel):
        try:
            logger.info("Creating the user: %s" % user)
            user_id = user.id
            if user.role.lower() == "admin":
                raise Exception("Not allowed to crate the admin role through API: %s" % user.role)
            cimpar_role = CimparRole.get({"id": user.role})
            if not cimpar_role:
                raise Exception("Given Role is not available with us %s" % user.role)
            if User.get({"id": user_id}):
                raise Exception("User Already Exist %s" % user.email)
            if len(cimpar_role) < 0:
                raise Exception("Unable to fetch the roles.")
            create_user = User(id=user_id, email=user.email, password=user.password)
            create_user.save()
            # Create access policy in Aidbox
            access_policy = AccessPolicy(
                engine="allow",
                link=[{"resourceType": "User", "id": user_id}]
            )
            access_policy.save()
            # Create Permission
            role_response = CimparPermission(
                id=generate_permission_id(user_id),
                user_id={"resourceType": "User", "id": user_id},
                cimpar_role={"resourceType": "CimparRole", "id": user.role}
            )
            role_response.save()
            return {"id": user_id, "email": user.email}
        except Exception as e:
            logger.error(f"Unable to create a user: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_token(token: TokenModel):
        try:
            resp = None
            logger.info("Creating the access token: %s" % token)
            res = API.make_request(method="GET", endpoint=f"/User?.email={token.username}", json=token.__dict__)
            if res.json()["total"] == 0:
                raise Exception("Given User Not Exist %s" % token.username)
            response = AidboxApi.open_request(method="POST", endpoint="/auth/token", json=token.__dict__)
            response.raise_for_status()
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token = response.json()["access_token"]
            user_id = res.json()["entry"][0]["resource"]["id"]
            permission_id = generate_permission_id(user_id)
            perm_res = API.make_request(method="GET", endpoint=f"/CimparPermission/{permission_id}")
            if perm_res.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User Permission not available"
                )
            role_name = perm_res.json()["cimpar_role"]["id"]
            return {"access_token": access_token, "role": role_name}
        except Exception as e:
            logger.error(f"Unable to create a token: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content=str(e),
                            status_code=status.HTTP_400_BAD_REQUEST)

