from fastapi import Response, status, HTTPException
from fastapi.responses import JSONResponse
import logging
import traceback
from aidbox.base import API

from models.auth_validation import (
    UserModel, TokenModel, RotateToken, User, AccessPolicy, CimparRole, CimparPermission, ChangePassword
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
            # logger.info("Creating the access token: %s" % token)
            # res = API.make_request(method="GET", endpoint=f"/User?.email={token.username}", json=token.__dict__)
            # if res.json()["total"] == 0:
            #     raise Exception("Given User Not Exist %s" % token.username)
            response = AidboxApi.open_request(method="POST", endpoint="/auth/token", json=token.__dict__)
            response.raise_for_status()
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            resp = response.json()
            user_id = resp.get("userinfo", {}).get("id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User ID not available"
                )
            permission_id = generate_permission_id(user_id)
            perm_res = API.make_request(method="GET", endpoint=f"/CimparPermission/{permission_id}")
            if perm_res.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User Permission not available"
                )
            resp["role"] = perm_res.json()["cimpar_role"]["id"]
            return resp
        except Exception as e:
            logger.error(f"Unable to create a token: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Check the username and password, unable to login"
            )

    @staticmethod
    def rotate_token(token: RotateToken):
        response = AidboxApi.open_request(method="POST", endpoint="/auth/token", json=token.__dict__)
        response.raise_for_status()
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        resp = response.json()
        return resp

    @staticmethod
    def change_password(change: ChangePassword):
        try:
            token = TokenModel(username=change.username, password=change.old_password,
                               client_id=change.client_id, grant_type=change.grant_type)
            resp = AuthClient.create_token(token)
            user_email = resp.get("userinfo", {}).get("email")
            user_id = resp.get("userinfo", {}).get("id")
            if not user_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Username or password is incorrect."
                )
            password_data = {
                "password": change.new_password,
            }
            response = API.make_request(method="PATCH", endpoint=f"/User/{user_id}", json=password_data)
            response.raise_for_status()
            return {"message": "Password updated successfully"}
        except Exception as e:
            logger.error(f"Unable to change the password: {str(e)}")
            logger.error(traceback.format_exc())
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=f"Unable to change the password: {str(e)}"
            )

    @staticmethod
    def logout():
        response = AidboxApi.make_request(method="DELETE", endpoint="/Session")
        response.raise_for_status()
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        resp = response.json()
        return resp

