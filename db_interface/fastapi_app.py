import uvicorn
from fastapi import FastAPI
from db_interface.routes.fastapi_rest_requests import router


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    print('Have been started.')


if __name__ == '__main__':
    uvicorn.run("fastapi_app:app", port=1112, host='127.0.0.1')
