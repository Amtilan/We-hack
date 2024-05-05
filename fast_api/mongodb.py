from pymongo import MongoClient
from pymongo.collection import Collection
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    email: EmailStr
    username : Field(..., min_length=3, max_length=20)
    password: str 

class MongoDBManager:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def insert_user(self, user_data: User):
        if self.collection.find_one({"email": user_data.email}):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.collection.find_one({"username": user_data.username}):
            raise HTTPException(status_code=400, detail="Username already taken")
        self.collection.insert_one(user_data.dict())
        return "User registered successfully"
    
