from fastapi import APIRouter, status, HTTPException, Depends
from database import Session, engine
from models import User
from schemas import SignupModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)

@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {"message": "hello"}

@auth_router.post('/signup', response_model=SignupModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    hashed_password = generate_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return new_user

@auth_router.post('/login',status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    hashed_password = str(db_user.password)  
    if not check_password_hash(hashed_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    access_token = Authorize.create_access_token(subject=hashed_password)
    refresh_token = Authorize.create_refresh_token(subject=hashed_password)

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return jsonable_encoder(response)

@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid refresh token")
    current_user = Authorize.get_jwt_subject()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    new_access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access_token": new_access_token})
