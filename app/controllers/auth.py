from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
#from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 

from ..schemas.auth import UserRegistrationInput, UserLoginInput, UserLoginOutput
from ..models.models import User
from ..database import get_db_session

router = APIRouter()

@router.post("/register")
def register(data: UserRegistrationInput):
    db = get_db_session()
    hashed_password = bcrypt.hash(data.password)
    user = User(username=data.username, password=hashed_password, name=data.name)

    try:
        db.add(user)
        db.commit()
        return {"message": "User registered successfully"}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username already exists")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=UserLoginOutput)
def login(data: UserLoginInput):
    db = get_db_session()
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not bcrypt.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return UserLoginOutput(id=user.id, name=user.name, username=user.username, jwt_token="token")
    