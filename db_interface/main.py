from db_interface.create_database import create_database
from db_interface.models.database import clear_db


if __name__ == '__main__':
    clear_db()
    create_database(load_fake_data=True, users=True)
