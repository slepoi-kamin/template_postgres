import inspect
import json
from aiohttp import web
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
        k: arg_types[k](v)
        for k, v in query.items()
        if k in arg_types
    }


def create_attributes_dict_to_dump(obj):
    obj_attributes = vars(obj)
    for key in obj_attributes:
        if '_' == key[0]:
            obj_attributes.pop(key)
    return obj_attributes


def dumps_to_json(objects):
    if isinstance(objects, list):
        objects = [create_attributes_dict_to_dump(obj) for obj in objects]
    return json.dumps(objects)


def dal(decorator, decorator_args):
    def actual_decorator(func):
        @decorator(decorator_args)
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
async def get_users_sessions(service: DAL = get_dal):
    return {'hello': 'world'}


@dal(routes.get, '/user/get_users_trade_sessions_info')
async def get_users_sessions(user_id: int, service: DAL = get_dal):
    sessions = await service.get_user_sessions(user_id)
    return [TradeSessionSchema(id=s.id, name=s.name, user_id=s.user_id) for s in sessions]


app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app, host='localhost', port=1111)


