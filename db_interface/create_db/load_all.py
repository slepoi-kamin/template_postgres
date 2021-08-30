import asyncio

from db_interface.create_db.sql import create_pool

loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())
