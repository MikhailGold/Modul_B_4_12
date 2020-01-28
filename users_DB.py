import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key = True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

def connect_db():
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    
    Base.metadata.create_all(engine)
    # создаем фабрику сессий
    Session = sessionmaker(engine)
    # возвращаем сессию
    return Session()

def request_data():
    """
        Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Введите пол (Male/Female) -: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("Введите день рождения (гггг-мм-дд) -: ")
    height = float(input("Введите рост (Пример - 1.77)-: "))
    # создаем нового пользователя
    user = User(first_name=first_name, last_name=last_name,
        gender = gender, email = email,  birthdate = birthdate,
        height = height
    )
    # возвращаем созданного пользователя
    return user  
def print_record(userRec):
    print(userRec.id, userRec.first_name, userRec.last_name, userRec.gender, userRec.email, userRec.birthdate, userRec.height)


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    mode = ""
    # просим пользователя выбрать режим
    while (mode != "3"):
        # проверяем режим
        mode = input("Выбери режим:\n1 - Ввести данные нового пользователя\n2 - Вывести всех имеющихся пользователей\n3 - Выход\n>>> ")
        if mode == "2":
            usersList = session.query(User).all()
            if (len(usersList) > 0):
                print("=============== Данные пользователей ====================")
                for userRec in usersList:
                    print_record(userRec)
                print("=========================================================")
                x = input("Нажмите Enter для продолжения !!!")
            else:
                print("В таблице отсутствуют данные!")
                x = input("Нажмите Enter для продолжения !!!")
            
        elif mode == "1":
            # запрашиваем данные пользоватлея
            userRec = request_data()
            # добавляем нового пользователя в сессию3
            session.add(userRec)
            # сохраняем все изменения, накопленные в сессии
            session.commit()
            print("Спасибо, данные сохранены!")
if __name__ == "__main__":
    main()