from fastapi import FastAPI
from authroutes import auth_router
from orderroutes import order_router
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")


app=FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 15

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)
