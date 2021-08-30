from pydantic import BaseModel


class TradeSessionSchema(BaseModel):
    id: int
    name: str
    user_id: int