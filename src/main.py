from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routes
from database import models
from database.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.meta())
