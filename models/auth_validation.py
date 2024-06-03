from pydantic import BaseModel, Field
from aidbox.base import DomainResource, BackboneElement


class UserModel(BaseModel):
    email: str
    password: str
    role: str = "patient"


class TokenModel(BaseModel):
    client_id: str = Field(default="cimpar-client-jwt", exclude=True)
    grant_type: str = Field(default="password", exclude=True)
    username: str
    password: str


class User(DomainResource):
    email: str
    password: str


class UserLink(BackboneElement):
    resourceType: str


class AccessPolicy(DomainResource):
    engine: str = "allow"
    link: list[UserLink] = []


class PermissionEndpoint(BaseModel):
    uri: str
    action: list[str]


class Permission(BaseModel):
    engine: str
    endpoints: list[PermissionEndpoint]


class CimparRole(DomainResource):
    resourceType: str
    id: str
    name: str
    permissions: list[Permission]


class CimparPermission(DomainResource):
    user_id: UserLink
    cimpar_role: UserLink

