from app.infrastructure.conn_db import ConectDatabase
from app.settings.adapters.models.models import Role
from app.settings.adapters.exceptions.exceptions import EntitiesNotFound

session = ConectDatabase.getInstance()

def validate_existence_role(id: str):
    role = session.get(Role, id)
    if not role:
        EntitiesNotFound(id)
    return True