from pymongo import MongoClient
from pymongo.collection import Collection
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    password: str

class MongoDBManager:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def insert_user(self, user_data: User):
        user_data.password = self.hash_password(user_data.password)
        if self.collection.find_one({"email": user_data.email}) or self.collection.find_one({"username": user_data.username}):
            raise HTTPException(status_code=400, detail="Username or email already registered")
        self.collection.insert_one(user_data.dict())
        return "User registered successfully"

    def authenticate_user(self, username: str, password: str):
        user = self.collection.find_one({"username": username})
        if not user:
            return False
        if not self.verify_password(password, user["password"]):
            return False
        return user

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)