import inspect
import json
from aiohttp import web
from db_interface.models import User
from typing import List, Optional
from db_interface.depends import get_dal
from db_interface.schemas.schemas import TradeSessionSchema
from db_interface.requests.async_requests import DAL

routes = web.RouteTableDef()


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_args_kwargs_types(func):
    signature = inspect.signature(func)
    return {
        par.name: par.annotation
        for par in signature.parameters.values()
        if par.default is inspect.Parameter.empty
    }


def get_args_from_request(func, request):
    query = request.query
    arg_types = get_args_kwargs_types(func)
    return {
        k: (arg_types[k](v) if v != 'false' else False)
        for k, v in query.items()
        if k in arg_types
    }


def create_attributes_dict_to_dump(obj):
    obj_attributes = vars(obj)
    keys_to_pop = [key for key in obj_attributes if '_' == key[0]]
    return {k: v for k, v in obj_attributes.items() if k not in keys_to_pop}


def dumps_to_json(objects):
    if isinstance(objects, list):
        objects = [create_attributes_dict_to_dump(obj) for obj in objects]
    elif hasattr(objects, '__dict__'):
        objects = create_attributes_dict_to_dump(objects)
    return json.dumps(objects)


def dal(decorator, *decorator_args, **decorator_kwargs):
    def actual_decorator(func):
        @decorator(*decorator_args, **decorator_kwargs)
        async def wrapper(*args, **kwargs):
            default_kwargs = get_default_args(func)
            request = args[0]
            args = args[1:]
            request_kwargs = get_args_from_request(func, request)
            if 'service' in default_kwargs.keys() and default_kwargs['service']:
                generator_function = default_kwargs['service']
                results_list = []
                async for yield_value in generator_function():
                    result = await func(*args, service=yield_value, **request_kwargs, **kwargs)
                    results_list.append(result)
                return web.Response(body=dumps_to_json(results_list[0]))
        return wrapper
    return actual_decorator


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


app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app, host='localhost', port=1111)


