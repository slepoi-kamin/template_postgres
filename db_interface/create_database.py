from faker import Faker
from sqlalchemy.orm import Session
import pickle
from db_interface.models.database import create_db, engine
from db_interface.models.lesson import Lesson
from db_interface.models.student import Student
from db_interface.models.group import Group
from db_interface.models.user import User
from db_interface.models.tradesession import TradeSession


def create_database(load_fake_data: bool = True, users: bool = True):
    create_db()
    if load_fake_data:
        session = Session(engine)
        _load_fake_users(session) if users else _load_fake_data(session)


def _load_fake_users(session):
    faker = Faker()
    for _ in range(10):
        user_id = faker.iana_id()
        user_name = faker.user_name()
        chat_id = user_id
        referral_id = faker.iana_id()
        user = User(user_id, user_name, chat_id, referral_id)
        session.add(user)
        session.flush()

        for __ in range(faker.random_int(1,3)):
            name = faker.cryptocurrency_name()
            ses = pickle.dumps(object())
            session.add(TradeSession(name, ses, user.id))
    session.commit()
    session.close()


def _load_fake_data(session: Session):
    lessons_names = ['Математика', 'Программирование', 'Философствуем за кружечкой пенного',
                     'Алгоритмы и структуры данных', 'Линейная алгебра', 'Мат. статистика',
                     'Физкультура']
    group1 = Group(group_name='1-МДА-7')
    group2 = Group(group_name='1-МДА-9')
    session.add(group1)
    session.add(group2)

    for key, it in enumerate(lessons_names):
        lesson = Lesson(lesson_title=it)
        lesson.groups.append(group1)
        if key % 2 == 0:
            lesson.groups.append(group2)
        session.add(lesson)

    faker = Faker('ru_RU')
    group_list = [group1, group2]
    session.commit()

    for _ in range(5):
        full_name = faker.name().split(' ')
        age = faker.random.randint(16, 25)
        address = faker.address()
        group = faker.random.choice(group_list)
        student = Student(full_name, age, address, group.id)
        session.add(student)

    session.commit()
    session.close()
