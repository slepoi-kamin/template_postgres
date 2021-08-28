import pickle
from sqlalchemy.orm import Session
from db_interface.models.database import engine
from db_interface.models.user import User
from db_interface.models.tradesession import TradeSession as TS, TradeSession
from sqlalchemy import and_, or_


def get_user(user_id):
    return session.query(User).filter(User.user_id == user_id).one()


def get_state(user_id):
    return get_user(user_id).state


def get_id_in_users(user_id):
    return get_user(user_id).id


def set_state(user_id, state: bool):
    user = get_user(user_id)
    user.state = state
    # TODO: add session.commit()
    return state


def _get_sessions_info(user_id):
    sessions = get_user_sessions(user_id)
    return ''.join([f'{str(it.id)} | {it.name}\n' for it in sessions])


def get_user_sessions(user_id):
    sessions_query = get_sessions_query(user_id)
    sessions = sessions_query.all()
    return sessions


def get_sessions_query(user_id):
    id_in_users = get_id_in_users(user_id)
    sessions_query = session.query(TS).filter(TS.user_id == id_in_users)
    return sessions_query


def add_session(user_id, session_name, session_object):
    id_in_users = get_id_in_users(user_id)
    dumped_session = pickle.dumps(session_object)
    session.add(TradeSession(session_name, dumped_session, id_in_users))
    # TODO: add session.commit()


def rm_session(user_id, session_name):
    sessions_query = get_sessions_query(user_id)
    return sessions_query.filter_by(name=session_name).delete()


def _get_table_info(table):
    count = session.query(table).count()
    return [raw for raw in session.query(table).filter(or_(table.id < 6, table.id > count-5))]


if __name__ == '__main__':
    session = Session(engine)
    uid = session.query(User).get(2).user_id
    pass