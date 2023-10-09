from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.infrastructure.conn_db import ConectDatabase
from dotenv import dotenv_values
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.settings.adapters.models.models import User as UserDatabase
from app.settings.adapters.exceptions.exceptions import UnauthorizedException, InactivateUser
from app.settings.adapters.serializer.serializer import PermissionsSchema, permissionSchema
from app.settings.adapters.services.servicesroles import get_role
from app.settings.adapters.services.servicespermissions import get_permission

session = ConectDatabase.getInstance()
values = dotenv_values('.env')

SECRET_KEY = values.get('SECRET_KEY')
ALGORITHM = values.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = values.get('ACCESS_TOKEN_EXPIRE_MINUTES')
SECRET_KEY_REFRESH = values.get('SECRET_KEY_REFRESH')


# Models

class TokenData(BaseModel):
    email: str | None = None

class User(BaseModel):
    username: str | None = None
    email: str
    full_name: str | None = None
    status: bool | None = None

class UserInDb(User):
    hashed_password: str
    permissions: list

class Token(BaseModel):
    access_token: str
    token_type: str



# Variables
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
 
def get_user(email: str):
    user = session.scalars(select(UserDatabase).filter(UserDatabase.email == email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CREDENCIALES_INVALIDAS")
    
    role = get_role(user.id_role)

    list_permissions = []
    for n in role.Permissions:
        permission = get_permission(n.id_permission)
        schema_permission = permissionSchema(permission)
        list_permissions.append(schema_permission["name"])
    
    return UserInDb(
        username=user.username, 
        full_name=user.fullname,
        email = user.email,
        status= user.status,
        hashed_password=user.hashed_password,
        permissions=list_permissions
    )
    
def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=60*24*30)})
    refresh_token = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return refresh_token


async def get_current_user(token: str = Depends(oauth_2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            UnauthorizedException()
        
        token_data = TokenData(email=email)
        
    except JWTError:
        UnauthorizedException() 

    user = get_user(token_data.email)
    if user is None:
        UnauthorizedException()
    return user


async def get_current_activate_user(current_user: UserInDb = Depends(get_current_user)):
    if current_user.status  == False:
        InactivateUser()
    return current_user

def verify_token(token: str = Depends(oauth_2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False