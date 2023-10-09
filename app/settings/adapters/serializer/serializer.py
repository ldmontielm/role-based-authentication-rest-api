from app.settings.adapters.models.models import Role, PermissionsRoles, Permission

def roleSchema(role: Role)-> dict:
    return{
        "id":role.id,
        "name":role.name,
        "status":role.status,
        "permissions": role.Permissions
    }

def rolesSchema(roles: list[Role])->list:
    return[roleSchema(role) for role in roles]


def permissionRolesSchema(permisisonsroles: PermissionsRoles)-> dict:
    return{
        "id_role":permisisonsroles.id_role,
        "id_permission":permisisonsroles.id_permission
   
    }

def permissionsRolesSchema(permissionsroles: list[PermissionsRoles])-> list:
    return[permissionRolesSchema(permissionsroles) for permissionsroles in permissionsroles]


def permissionSchema(permission: Permission):
    return {
        "id":permission.id,
        "name":permission.name,
    }
    
def PermissionsSchema(permissions: list[Permission])->list:
    return[permissionSchema(permission) for permission in permissions]
