from fastapi import APIRouter 
from passlib.hash import bcrypt

from ..schemas.auth import UserRegistrationInput
from ..models.models import User
from ..database import get_db_session

router = APIRouter()

@router.post("/register")
def register(data: UserRegistrationInput):
    db = get_db_session()
    hashed_password = bcrypt.hash(data.password)
    user = User(username=data.username, password=hashed_password, name=data.name)

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}, 200
    