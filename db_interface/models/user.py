from sqlalchemy import Column, VARCHAR, Integer, Boolean
from db_interface.models.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    user_name = Column(VARCHAR(100))
    chat_id = Column(Integer)
    referral_id = Column(Integer)
    state = Column(Boolean)
    session = relationship('TradeSession')

    def __init__(self, user_id: int, user_name: str, chat_id: int, referal_id: int = None):
        self.state = False
        self.user_id = user_id
        self.user_name = user_name
        self.chat_id = chat_id
        self.referral_id = referal_id

    def __repr__(self):
        info: str = f'{self.id} # User ' \
                    f'[user id: {self.user_id}, ' \
                    f'user name: {self.user_name}, ' \
                    f'chat id: {self.chat_id}, ' \
                    f'referal id: {self.referral_id}, ' \
                    f'current state: {self.state}]'
        return info
