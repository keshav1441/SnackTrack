from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

class Token(BaseModel):
    access_token: str
    token_type: str

class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool]
    is_staff: Optional[bool]    
    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {  
                "username": "KeshavSharma",
                "email": "keshavsharma1441@gmail.com",
                "password": "password",
                "is_active": True,
                "is_staff": False
            }
        }
        
class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 30

    
class LoginModel(BaseModel):
    username: str
    password: str
    
        