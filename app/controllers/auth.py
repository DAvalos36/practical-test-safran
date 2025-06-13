from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
#from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 

from ..schemas.auth import UserRegistrationInput
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

    