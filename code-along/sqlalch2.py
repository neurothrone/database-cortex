# from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB_NAME = load_dotenv("DB")
# DB_PROTOCOL = load_dotenv("PROTOCOL")
# DB_USER = load_dotenv("USERNAME")
# DB_PASS = load_dotenv("PASSWORD")
# HOST = load_dotenv("HOST")
# PORT = load_dotenv("PORT")

DB_NAME = "py-db"
DB_PROTOCOL = "mysql+mysqlconnector"
DB_USER = "admin"
DB_PASS = "super-secret-password"
HOST = "localhost"
PORT = "3306"

engine = sqlalchemy.create_engine(
    url=f"{DB_PROTOCOL}://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}"
)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

PERSON_TABLE = "car_owners"
CAR_TABLE = "autos"


class Person(Base):
    __tablename__ = PERSON_TABLE

    id_persons = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(100))

    cars = sqlalchemy.orm.relationship("Car", back_populates="owner")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id_persons={self.id_persons}, name={self.name}, surname={self.surname})"

    def __str__(self) -> str:
        return f"{self.id_persons} - {self.name} {self.surname} - {self.cars}"

    @staticmethod
    def create(name: str, surname: str, commit: bool = True) -> "Person":
        person = Person(name=name, surname=surname)
        session.add(person)
        if commit:
            session.commit()
        else:
            session.rollback()
        return person

    @staticmethod
    def find_all() -> list["Person"]:
        return session.query(Person).all()

    @staticmethod
    def find_by_id(pk: int) -> "Person":
        return session.query(Person).filter(Person.id_persons == pk).first()

    @staticmethod
    def print_all() -> None:
        for person in Person.find_all():
            print(person)

    @staticmethod
    def change_car_owner() -> bool:
        pass


class Car(Base):
    __tablename__ = CAR_TABLE

    id_cars = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    reg_no = sqlalchemy.Column(sqlalchemy.String(7), nullable=False)
    model = sqlalchemy.Column(sqlalchemy.String(50))
    color = sqlalchemy.Column(sqlalchemy.String(50))

    # parameters: referenced data_type, referenced table.col_name
    id_owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(f"{PERSON_TABLE}.id_persons"))
    # parameters: class_name, name of Person class relationship variable, in this case 'cars'
    owner = sqlalchemy.orm.relationship("Person", back_populates="cars")

    def __repr__(self) -> str:
        return f"{self.reg_no} - {self.model}"

    @staticmethod
    def find_all() -> list["Car"]:
        return session.query(Car).all()

    @staticmethod
    def find_by_id(pk: int) -> "Car":
        return session.query(Car).filter(Car.id_cars == pk).first()

    @staticmethod
    def print_all() -> None:
        for car in Car.find_all():
            print(car)


def main() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
