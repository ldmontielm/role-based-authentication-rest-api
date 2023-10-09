from sqlalchemy import select
from app.infrastructure.conn_db import ConectDatabase
from app.settings.adapters.exceptions.exceptions import EntitiesNotFound
from app.settings.adapters.models.models import Permission

session = ConectDatabase.getInstance()

def get_permissions():
    permissions = session.scalars(select(Permission)).all()
    if len(permissions) == 0:
        return []
    return permissions

def get_permission(id:str):
    permission = session.get(Permission, id)
    if not permission:
        EntitiesNotFound("permission")
    return permission 