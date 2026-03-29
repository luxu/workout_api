from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB_URL: str = Field(
    #     default='postgresql+asyncpg://workout:workout@localhost/workout'
    # )
    DB_URL: str = Field(default='sqlite+aiosqlite:///./workout.db')


settings = Settings()
