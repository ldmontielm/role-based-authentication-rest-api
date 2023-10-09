from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.conn_db import ConectDatabase
from app.settings.adapters.models.models import Role, PermissionsRoles
from app.settings.adapters.exceptions.exceptions import NotCreatedEntity, EntitiesNotFound, CouldNotAssociateEntities
from app.settings.domain.models.models import RoleCreate
from app.settings.adapters.validations.roles_validations import validate_existence_role
from app.settings.adapters.validations.permissions_validations import validate_existence_permission



session = ConectDatabase.getInstance()


def post_role(role_create: RoleCreate):
    role = Role(name=role_create.name)
    if not role:
        NotCreatedEntity(role_create.name)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def get_role(id:str):
    role = session.get(Role, id)
    if not role:
        EntitiesNotFound(id)
    return role

def get_roles():
    roles = session.scalars(select(Role)).all()
    if not roles:
        return []
    return roles

def assign_permissions():
    pass

def assign_permission(id_role: str, id_permission: str):
    if validate_existence_role(id_role) and validate_existence_permission(id_permission):
        permission_role = PermissionsRoles(id_role = id_role, id_permission = id_permission)
        session.add(permission_role)
        session.commit()
        return permission_role
    CouldNotAssociateEntities(id_role, id_permission)