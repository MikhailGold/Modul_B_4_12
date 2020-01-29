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

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key = True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

def connect_db():
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    
    Base.metadata.create_all(engine)
    # создаем фабрику сессий
    Session = sessionmaker(engine)
    # возвращаем сессию
    return Session()

def print_record_user(userRec):
    print(userRec.id, userRec.first_name, userRec.last_name, userRec.gender, userRec.email, userRec.birthdate, userRec.height)

def print_record_athelete(atheleteRec):
    print(atheleteRec.id, atheleteRec.name, atheleteRec.age, atheleteRec.birthdate, atheleteRec.gender, atheleteRec.height, atheleteRec.weight, 
    atheleteRec.gold_medals, atheleteRec.silver_medals, atheleteRec.bronze_medals, atheleteRec.total_medals, atheleteRec.sport, atheleteRec.country)

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    mode = ""
    # просим пользователя выбрать режим
    while (mode != "3"):
        # проверяем режим
        mode = input("Выбери режим:\n1 - Ввести ID пользователя\n2 - Вывести всех имеющихся пользователей\n3 - Выход\n>>> ")
        if mode == "1":
            id_user = int(input("Введите ID для поиска пользователя: "))
            ourUser = session.query(User).filter(User.id==id_user).first()
            if (ourUser != None):
                print("================ Данные пользователя  ====================")
                print_record_user(ourUser)
                print("==========================================================")
            
                print("==================== Данные атлетов  ====================")
                way = input("Выберете критерии отбора атлетов:\n1 - В сторону увеличения\n2 - В сторону уменьшения\n>>>")
                if (way == "1"):
                    # Задаем поиск по критериям, сортируем в сторону возрастания и берем только первый элемент
                    athelete1 = session.query(Athelete).filter(Athelete.birthdate>ourUser.birthdate).order_by(Athelete.birthdate).first()
                    athelete2 = session.query(Athelete).filter(Athelete.height>ourUser.height).order_by(Athelete.height).first()
                    if (athelete1 != None):
                        print_record_athelete(athelete1)
                    if(athelete2 != None):
                        print_record_athelete(athelete2)
                    print("=========================================================")
                    x = input("Нажмите Enter для продолжения !!!")
                elif (way == "2"): 
                    # Задаем поиск по критериям, сортируем в сторону убывания и берем только первый элемент
                    athelete1 = session.query(Athelete).filter(Athelete.birthdate<ourUser.birthdate).order_by(Athelete.birthdate.desc()).first()
                    athelete2 = session.query(Athelete).filter(Athelete.height<ourUser.height).order_by(Athelete.height.desc()).first()
                    if (athelete1 != None):
                        print_record_athelete(athelete1)
                    if(athelete2 != None):
                        print_record_athelete(athelete2)
                    print("=========================================================")
                    x = input("Нажмите Enter для продолжения !!!")
                else:
                    print("Неверный ввод. Ничего не будет отображено!")
            else:
                print("Пользователя с таким идентификатором нет!")
                x = input("Нажмите Enter для продолжения !!!")
        elif mode == "2":
            usersList = session.query(User).all()
            if (len(usersList) > 0):
                print("=============== Данные пользователей ====================")
                for userRec in usersList:
                    print_record_user(userRec)
                print("=========================================================")
                x = input("Нажмите Enter для продолжения !!!")
            else:
                print("В таблице отсутствуют данные!")
                x = input("Нажмите Enter для продолжения !!!")
if __name__ == "__main__":
    main()