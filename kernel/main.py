from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import api_router

app = FastAPI(title='WorkoutApi', debug=True)
app.include_router(api_router)
add_pagination(app)

"""
uv run uvicorn kernel.main:app --reload --port 8001
"""
