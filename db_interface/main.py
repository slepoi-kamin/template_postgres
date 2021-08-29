import asyncio
from fastapi import Depends
from db_interface.create_database import create_database
from db_interface.models.database import clear_db
from db_interface.models.async_database import get_session
from db_interface.requests import async_requests as service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

app = FastAPI()



@app.get("/get_users_sessions/{user_id}")
async def get_users_sessions(user_id: int, session: AsyncSession = Depends(get_session)):
    sessions = await service.get_user_sessions(user_id, session=session)
    return {"Hello": "World"}


@app.get("/")
async def get_users_sessions():
    return {"Hello": "World"}


if __name__ == '__main__':
    pass
