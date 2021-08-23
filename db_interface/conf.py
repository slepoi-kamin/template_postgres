import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")