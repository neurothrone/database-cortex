import os

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_NAME = "classicmodels"
DB_PROTOCOL = os.getenv("DB_PROTOCOL")
DB_USER = "car-user"
DB_PASS = "1234"
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

engine = sqlalchemy.create_engine(
    url=f"{DB_PROTOCOL}://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}"
)

Base = automap_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# reflect: takes a look on the database and generates matching classes
Base.prepare(engine, reflect=True)


def to_str(self) -> str:
    attributes: dict = self.__dict__
    if isinstance(self, Base):
        attributes.pop("_sa_instance_state")

    attr_to_list = []
    for key, value in attributes.items():
        attr_to_list.append(f"{key}={value}")

    attr_to_str = "\n".join(attr_to_list)
    return f"{self.__class__.__name__}({attr_to_str})"


for cls in Base.classes:
    cls.__repr__ = to_str

# change names of the auto-generated classes
Customer = Base.classes.customers
Employees = Base.classes.employees
Offices = Base.classes.offices
OrderDetail = Base.classes.orderdetails
Order = Base.classes.orders
Payment = Base.classes.payments
ProductLine = Base.classes.productlines
Product = Base.classes.products

# print(Base.classes.orders.__name__)

for cls in Base.classes:
    print(cls)


def customer_repr(self) -> str:
    return f"{self.customerName}, {self.contactFirstName} {self.contactLastName}. {self.country}"


# Customer.__repr__ = customer_repr

# from sqlalch import BaseModel
# Customer.__repr__ = BaseModel.to_str
# Customer.__repr__ = to_str


def main():
    exit()
    # customers = session.query(Customer).all()

    target_customer = "GiftsForHim.com"
    customer = session.query(Customer).filter(Customer.customerName == target_customer).first()
    # print(customer)

    for order in customer.orders_collection:
        print(order)
        print(order.orderNumber)
        for order_row in order.orderdetails_collection:
            print(f"\t{order_row.products.productName}")
            print(f"\t\tPrice each: ${order_row.priceEach}, Quantity: {order_row.quantityOrdered}")
            print(
                f"\t\t\tTotal: ${order_row.priceEach * order_row.quantityOrdered:,}")  # :, specifies american notation
        # if order_row.productName == target_product:


# for customer in customers:
#     # print(customer)  # <sqlalchemy.ext.automap.customers object at 0x000..."
#     print(customer.customerName)


if __name__ == "__main__":
    main()
