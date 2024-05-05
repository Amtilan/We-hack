from fastapi import APIRouter, HTTPException, Depends, status
from mongodb import MongoDBManager, User, Token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

db_manager = MongoDBManager(os.getenv('MONGO_API_KEY'), "mydatabase", "users")


@router.post("/register/")
async def register(user: User):
    return db_manager.insert_user(user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user