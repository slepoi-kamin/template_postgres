import asyncio
import socket
from typing import List, Optional

import uvicorn
from fastapi import Depends
from db_interface.create_database import create_database
from db_interface.depends import get_dal
from db_interface.models.database import clear_db
from db_interface.models import async_session, TradeSession, User
from db_interface.requests.async_requests import DAL
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TradeSessionSchema(BaseModel):
    id: int
    name: str
    user_id: int


@app.get("/user/get_users_trade_sessions_info")
async def get_users_sessions(user_id: int, service: DAL = Depends(get_dal)) -> List[TradeSessionSchema]:
    sessions = await service.get_user_sessions(user_id)
    return [TradeSessionSchema(id=s.id, name=s.name, user_id=s.user_id) for s in sessions]


@app.get("/user/get_user")
async def get_user(user_id: int, service: DAL = Depends(get_dal)) -> User:
    return await service.get_user(user_id)


@app.get("/user/get_state")
async def get_state(user_id: int, service: DAL = Depends(get_dal)) -> bool:
    return await service.get_state(user_id)


@app.get("/user/get_global_user_id")
async def get_global_user_id(user_id: int, service: DAL = Depends(get_dal)) -> int:
    return await service.get_id_in_users(user_id)


@app.get("/user/get_table_partial")
async def get_table_partial(service: DAL = Depends(get_dal)) -> List[User]:
    return await service.get_table_info(User)


@app.post("/user/add_user")
async def add_user(user_id: int, user_name: str, chat_id: int,
                   referral_id: Optional[int] = None, service: DAL = Depends(get_dal)):
    return await service.add_user(user_id, user_name, chat_id, referral_id)


@app.patch("/user/set_state")
async def set_state(user_id: int, state: bool, service: DAL = Depends(get_dal)):
    return await service.set_state(user_id, state)


@app.delete("/session/delete")
async def del_session(user_id: int, session_name: str, service: DAL = Depends(get_dal)):
    sessions_to_delete = await service.rm_session(user_id, session_name)
    return [TradeSessionSchema(id=s.id, name=s.name, user_id=s.user_id) for s in sessions_to_delete]


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')
