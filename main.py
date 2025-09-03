#this is the main file, contain api/endpoints that we uses.
from fastapi import FastAPI
from database import engine
from routers import auth, bookstore
import models




app = FastAPI()
app.include_router(auth.router)
app.include_router(bookstore.router)

models.Base.metadata.create_all(bind=engine)


