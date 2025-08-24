import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

import models
from api import router
from database import engine

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "daven-boparai-knotch-take-home")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# Create tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Knotch Take Home Challenge: Content Leaderboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
