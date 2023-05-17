from routes.app_routes import home
from fastapi import FastAPI

app = FastAPI()

app.include_router(home)
