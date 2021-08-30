import asyncio
import pickle
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from db_interface.models import async_engine
from db_interface.models.async_database import async_session
from db_interface.models import User
from db_interface.models import TradeSession as TS
from sqlalchemy import or_, func, select, insert


class DAL:

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_user(self, user_id: int) -> User:
        result = await self.db_session.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().one()
        return user

    async def get_state(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        return user.state

    async def get_id_in_users(self, user_id: int) -> int:
        user = await self.get_user(user_id)
        return user.id

    async def set_state(self, user_id: int, state: bool):
        user = await self.get_user(user_id)
        user.state = state
        await self.db_session.commit()
        return state

    async def _get_sessions_info(self, user_id: int):
        sessions = await self.get_user_sessions(user_id)
        return ''.join([f'{str(it.id)} | {it.name}\n' for it in sessions])

    async def get_user_sessions(self, user_id: int):
        id_in_users = await self.get_id_in_users(user_id)
        result = await self.db_session.execute(select(TS).where(TS.user_id == id_in_users))
        return result.scalars().all()

    async def add_session(self, user_id: int, session_name: str, session_object):
        id_in_users = await self.get_id_in_users(user_id)
        dumped_session = pickle.dumps(session_object)
        user_session = TS(session_name, dumped_session, id_in_users)
        self.db_session.add(user_session)
        await self.db_session.commit()
        return user_session

    async def add_user(self, user_id, user_name, chat_id, referral_id=None):
        user = User(user_id, user_name, chat_id, referral_id)
        self.db_session.add(user)
        await self.db_session.commit()
        return user

    async def rm_session(self, user_id: int, session_name):
        user_sessions = await self.get_user_sessions(user_id)
        sessions_to_delete = [s for s in user_sessions if s.name == session_name]
        [await self.db_session.delete(s) for s in sessions_to_delete]
        await self.db_session.commit()
        return sessions_to_delete

    async def get_table_info(self, table) -> List[User]:
        count = await self.get_table_count(table)
        result = await self.db_session.execute(select(table).where(or_(table.id < 6, table.id > count - 5)))
        return result.scalars().all()

    async def get_table_count(self, table):
        count_result = await self.db_session.execute(select(func.count(table.id)))
        count = count_result.scalars().one()
        return count


if __name__ == '__main__':
    pass
