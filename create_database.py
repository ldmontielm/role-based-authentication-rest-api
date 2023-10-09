from app.infractucture.conn_db import engine, Base
from app.settings.adapters.models.models import Permission, Role, PermissionsRoles

Base.metadata.create_all(engine)