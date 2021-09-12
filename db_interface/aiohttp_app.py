from aiohttp import web
from db_interface.routes.aiohttp_rest_requests import routes


app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app, host='localhost', port=1111)
