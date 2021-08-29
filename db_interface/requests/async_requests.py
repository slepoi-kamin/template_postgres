import asyncio
import pickle
from sqlalchemy.ext.asyncio import AsyncSession
from db_interface.models import async_engine
from db_interface.models.async_database import async_session
from db_interface.models import User
from db_interface.models import TradeSession as TS
from sqlalchemy import or_, func, select


async def get_user(session, user_id: int) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalars().one()
    return user


async def get_state(session, user_id: int):
    user = await get_user(session, user_id)
    return user.state


async def get_id_in_users(session, user_id: int):
    user = await get_user(session, user_id)
    return user.id


async def set_state(session, user_id: int, state: bool):
    user = await get_user(session, user_id)
    user.state = state
    await session.commit()
    return state


async def _get_sessions_info(session, user_id: int):
    sessions = await get_user_sessions(session, user_id)
    return ''.join([f'{str(it.id)} | {it.name}\n' for it in sessions])


async def get_user_sessions(session, user_id: int):
    id_in_users = await get_id_in_users(session, user_id)
    result = await session.execute(select(TS).where(TS.user_id == id_in_users))
    sessions = result.scalars().all()
    return sessions


async def add_session(session, user_id: int, session_name: str, session_object):
    id_in_users = await get_id_in_users(session, user_id)
    dumped_session = pickle.dumps(session_object)
    user_session = TS(session_name, dumped_session, id_in_users)
    session.add(user_session)
    await session.commit()
    return user_session


async def add_user(session, user_id, user_name, chat_id, referral_id=None):
    user = User(user_id, user_name, chat_id, referral_id)
    session.add(user)
    await session.commit()
    return user


async def rm_session(session, user_id: int, session_name):
    user_sessions = await get_user_sessions(session, user_id)
    sessions_to_delete = [s for s in user_sessions if s.name == session_name]
    [await session.delete(s) for s in sessions_to_delete]
    await session.commit()
    return sessions_to_delete


async def _get_table_info(session, table):
    count = await get_table_count(session, table)
    result = await session.execute(select(table).where(or_(table.id < 6, table.id > count - 5)))
    return result.scalars().all()


async def get_table_count(session, table):
    count_result = await session.execute(select(func.count(table.id)))
    count = count_result.scalars().one()
    return count


if __name__ == '__main__':
    async def test():
        ses = async_session()
        uid = 991313
        await get_user(ses, uid)
        await add_user(ses, 1111111, 'aaaaaa', 1111111, uid)
        await add_session(ses, uid, 'aaaaaaa', object())
        await ses.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
