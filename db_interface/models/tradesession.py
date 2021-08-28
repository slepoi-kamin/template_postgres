from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from db_interface.models.database import Base


class TradeSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    session = Column(BYTEA)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    def __init__(self, name: str, session: bytes, user_id: int):
        self.name = name
        self.session = session
        self.user_id = user_id

    def __repr__(self):
        info: str = f'{self.id} # Session ' \
                    f'[name: {self.name}, ' \
                    f'user id: {self.user_id}]'
        return info
