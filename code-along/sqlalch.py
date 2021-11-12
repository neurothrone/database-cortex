import os

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_PROTOCOL = os.getenv("DB_PROTOCOL")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

engine = sqlalchemy.create_engine(
    url=f"{DB_PROTOCOL}://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}"
)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

PERSON_TABLE = "persons"
CAR_TABLE = "cars"


class BaseModel:
    def to_str(self) -> str:
        attributes: dict = self.__dict__
        undesired_attr = "_sa_instance_state"
        if isinstance(self, Base) and attributes.get(undesired_attr, None):
            attributes.pop(undesired_attr)

        attr_to_list = []
        for key, value in attributes.items():
            attr_to_list.append(f"{key}={value}")

        # attr_to_str = ', '.join({f{key: value for key, value in attributes.items()})
        return f"{self.__class__.__name__}({', '.join(attr_to_list)})"


class Person(Base, BaseModel):
    __tablename__ = PERSON_TABLE

    id_persons = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    cars = sqlalchemy.orm.relationship("Car", back_populates="owner")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id_persons={self.id_persons}, name={self.name}, surname={self.surname})"

    def __str__(self) -> str:
        return self.to_str()

        # cars = "\n".join([f'* {car}' for car in self.cars])
        # return f"{self.id_persons} - {self.name} {self.surname}:\n{cars}"

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
    def change_car_owner(person_from_id: int, person_move_id: int, car_index: int) -> bool:
        try:
            p1 = Person.find_by_id(person_from_id)
            p2 = Person.find_by_id(person_move_id)
            car = p1.cars[car_index]
            p1.cars.remove(car)
            p2.cars.append(car)
            # confirm modifications
            session.add(p1)
            session.add(p2)
            # save to database
            session.commit()
        except SQLAlchemyError as error:
            print(error)
            return False
        return True


class Car(Base, BaseModel):
    __tablename__ = "cars"

    id_cars = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    reg_no = sqlalchemy.Column(sqlalchemy.String(7), nullable=False)
    model = sqlalchemy.Column(sqlalchemy.String(50))

    # parameters: referenced data_type, referenced table.col_name
    id_owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(f"persons.id_persons"))
    # parameters: class_name, name of Person class relationship variable, in this case 'cars'
    owner = sqlalchemy.orm.relationship("Person", back_populates="cars")

    def __repr__(self) -> str:
        return f"Car(id_cars={self.id_cars}, reg_no={self.reg_no}, model={self.model})"

    def __str__(self) -> str:
        return self.to_str()
        # return f"{self.reg_no} - {self.model}"

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
    Person.print_all()
    print("-" * 40)

    # base = BaseModel("zane", "cortex", 30)
    # print(base.to_str())

    # switch cars between two owners
    # Person.change_car_owner(1, 5, 1)
    # print("-" * 40)

    # Person.print_all()
    # print("-" * 40)

    # p1 = Person.create("zane", "cortex")


if __name__ == "__main__":
    main()
