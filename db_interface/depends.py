from db_interface.models import async_session
from db_interface.requests.async_requests import DAL


async def get_dal():
    async with async_session() as session:
        async with session.begin():
            yield DAL(session)
