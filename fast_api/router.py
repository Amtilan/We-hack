from fastapi import APIRouter, HTTPException, Depends, status
from mongodb import MongoDBManager, User, Token, oauth2_scheme, Schedule
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
    return {"access_token": user["email"], "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user

@router.post("/schedule/")
async def create_user_schedule(schedule: Schedule, current_user: User = Depends(oauth2_scheme)):
    if schedule.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to create schedule for other users")
    return db_manager.create_schedule(schedule.username, schedule.schedule_items)

@router.get("/schedule/{username}", response_model=Schedule)
async def read_user_schedule(username: str, current_user: User = Depends(oauth2_scheme)):
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to schedule denied")
    schedule = db_manager.get_schedule(username)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return schedule

@router.put("/schedule/")
async def update_user_schedule(schedule: Schedule, current_user: User = Depends(oauth2_scheme)):
    if schedule.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update schedule for other users")
    return db_manager.update_schedule(schedule.username, schedule.schedule_items)