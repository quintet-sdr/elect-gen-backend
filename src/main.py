from fastapi import FastAPI


import routes
from database import models
from database.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(routes.meta())
