from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    name : str
       
class Permission(PermissionBase):
    id: Optional[str]
    class Config:
        from_attributes = True

class PermissionCreate(PermissionBase):
    pass



class RoleBase(BaseModel):
    name : str
       
class Role(RoleBase):
    id: Optional[str]
    status:bool = True
    
    class Config:
        from_attributes = True

class RoleCreate(RoleBase):
    pass


class PermissionsRolesBase(BaseModel):
    id_role : str
    id_permission : str
    
class PermissionsRoles(PermissionsRolesBase):
    class Config:
        from_attributes = True

class PermissionsRolesCreate(PermissionsRolesBase):
    pass

class AssignPermissions(BaseModel):
    id_permission: str