from app.schemas.auth import UserRegistrationInput
from typing import Union
from app.controllers.auth import router
from app.controllers.predictions import router2

from fastapi import FastAPI

from app.database import create_tables

app = FastAPI()

app.include_router(router, prefix="/api", tags=["auth"])
app.include_router(router2, prefix="/api", tags=["predictions"])

create_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
