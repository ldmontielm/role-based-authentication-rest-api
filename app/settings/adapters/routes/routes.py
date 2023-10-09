from fastapi import APIRouter, Depends

from app.settings.adapters.services.servicesauth import User, authenticate_user, create_access_token, get_current_activate_user
from app.settings.adapters.services.servicespermissions import get_permission, get_permissions
from app.settings.adapters.services.servicesroles import post_role, get_role, get_roles, assign_permission
from app.settings.domain.models.models import RoleCreate
from app.settings.adapters.serializer.serializer import roleSchema
from app.settings.adapters.exceptions.exceptions import UnauthorizedException
from datetime import datetime, timedelta
from dotenv import dotenv_values




settings = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)
values = dotenv_values('.env')

ACCESS_TOKEN_EXPIRE_MINUTES = values.get('ACCESS_TOKEN_EXPIRE_MINUTES')



@settings.get('/get-roles')
async def getRoles():
    roles = get_roles()
    return {
        "roles" : roles
    }

@settings.get("/get-role/{id}")
async def getRole(id: str):
    role = get_role(id)
    return roleSchema(role)

@settings.post("/create-role")
async def createRole(role_create: RoleCreate):
    role = post_role(role_create)
    return role

@settings.get("/get-permissions")
async def getPermissions(current_user: User = Depends(get_current_activate_user)):
    permissions = get_permissions()
    return {
        "permissions" : permissions
    }

@settings.get('/get-permission/{id}')
async def getPermission(id: str):
    permission = get_permission(id)
    return permission

@settings.post('/assign-permission')
async def getPermission(id_role: str, id_permission: str):
    assign = assign_permission(id_role, id_permission)
    return {
        "assign": assign
    }



