from aiohttp import web
from db_interface.models import User
from typing import List, Optional
from db_interface.depends import get_dal
from db_interface.routes.aiohttp_request_handling import dal
from db_interface.schemas.schemas import TradeSessionSchema
from db_interface.requests.async_requests import DAL


routes = web.RouteTableDef()


@dal(routes.get, '/')
async def hello_world(service: DAL = get_dal):
    return {'hello': 'world'}


@dal(routes.get, '/user/get_users_trade_sessions_info')
async def get_users_sessions(user_id: int, service: DAL = get_dal) -> List[TradeSessionSchema]:
    sessions = await service.get_user_sessions(user_id)
    return [TradeSessionSchema(id=s.id, name=s.name, user_id=s.user_id) for s in sessions]


@dal(routes.get, '/user/get_user')
async def get_user(user_id: int, service: DAL = get_dal) -> User:
    return await service.get_user(user_id)


@dal(routes.get, '/user/get_state')
async def get_state(user_id: int, service: DAL = get_dal) -> bool:
    return await service.get_state(user_id)


@dal(routes.get, '/user/get_global_user_id')
async def get_global_user_id(user_id: int, service: DAL = get_dal) -> int:
    return await service.get_id_in_users(user_id)


@dal(routes.get, '/user/get_table_partial')
async def get_table_partial(service: DAL = get_dal) -> List[User]:
    return await service.get_table_info(User)


@dal(routes.post, '/user/add_user')
async def add_user(user_id: int, user_name: str, chat_id: int,
                   referral_id: Optional[int] = None, service: DAL = get_dal):
    return await service.add_user(user_id, user_name, chat_id, referral_id)


@dal(routes.patch, '/user/set_state')
async def set_state(user_id: int, state: bool, service: DAL = get_dal):
    return await service.set_state(user_id, state)


@dal(routes.delete, '/session/delete')
async def del_session(user_id: int, session_name: str, service: DAL = get_dal):
    sessions_to_delete = await service.rm_session(user_id, session_name)
    return [TradeSessionSchema(id=s.id, name=s.name, user_id=s.user_id) for s in sessions_to_delete]
