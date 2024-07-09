from fastapi import FastAPI

from src import routes

app = FastAPI()

app.include_router(routes.meta())
