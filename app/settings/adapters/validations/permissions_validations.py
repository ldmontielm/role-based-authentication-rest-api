from app.infrastructure.conn_db import ConectDatabase
from app.settings.adapters.models.models import Permission
from app.settings.adapters.exceptions.exceptions import EntitiesNotFound

session = ConectDatabase.getInstance()

def validate_existence_permission(id: str):
    permission = session.get(Permission, id)
    if not permission:
        EntitiesNotFound(id)
    return True