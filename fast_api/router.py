from fastapi import APIRouter
from mongodb import MongoDBManager, User
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

db_manager = MongoDBManager(os.getenv('MONGO_API_KEY'), "mydatabase", "users")


@router.post("/register/")
async def register(user: User):
    return db_manager.insert_user(user)

