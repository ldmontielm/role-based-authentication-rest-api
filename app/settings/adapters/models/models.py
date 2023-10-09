import  uuid
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app.infrastructure.conn_db import Base


class Permission(Base):
  __tablename__= "permissions"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)

  
class Role(Base):
  __tablename__= "roles"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  Permissions: Mapped[List["PermissionsRoles"]]= relationship()
  users: Mapped[List["User"]] = relationship(back_populates="role")
  
  
class PermissionsRoles(Base):
  __tablename__ ="permission_role"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  id_role : Mapped[str] = mapped_column(ForeignKey("roles.id"), primary_key=True)
  id_permission: Mapped[str] = mapped_column(ForeignKey("permissions.id"), primary_key=True)
  Permission: Mapped["Permission"] = relationship()

class User(Base):
  __tablename__ = "users"

  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  username: Mapped[str]= mapped_column(String(60), nullable=False)
  fullname: Mapped[str]= mapped_column(String(120), nullable=False)
  email: Mapped[str]= mapped_column(String(150), nullable=False)
  hashed_password: Mapped[str]= mapped_column(String(100), nullable=False)
  status: Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  id_role: Mapped[str] = mapped_column(ForeignKey("roles.id"))
  role: Mapped["Role"] = relationship(back_populates="users")

class Joda(Base):
  __tablename__ = "jodas"

  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  username: Mapped[str]= mapped_column(String(60), nullable=False)
  jaider: Mapped[str]= mapped_column(String(120), nullable=False)