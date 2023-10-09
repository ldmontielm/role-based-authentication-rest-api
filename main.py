from datetime import timedelta
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.settings.adapters.exceptions.exceptions import UnauthorizedException
from app.settings.adapters.services.servicesauth import Token, authenticate_user, create_access_token, get_current_activate_user, UserInDb, verify_token, create_refresh_token
from dotenv import dotenv_values
from fastapi.responses import JSONResponse

# Routes
from app.settings.adapters.routes.routes import settings

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

values = dotenv_values('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = values.get('ACCESS_TOKEN_EXPIRE_MINUTES')


app.include_router(settings)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        UnauthorizedException()

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token({"sub": user.email}, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/user/me")
async def get_current_user(user: UserInDb = Depends(get_current_activate_user)):
    return user