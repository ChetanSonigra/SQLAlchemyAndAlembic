from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.sqltypes import BIGINT, VARCHAR, TIMESTAMP, Integer, DECIMAL
from datetime import datetime
from sqlalchemy import func, ForeignKey
from typing import Any, Optional, Annotated
from database_connection import engine

class Base(DeclarativeBase):
    pass

class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(),server_default=func.now(),onupdate=func.now())

class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls)->str:
        return cls.__name__.lower() + "s"


# class User(Base, TimeStampMixin, TableNameMixin):

#     telegram_id: Mapped[int] = mapped_column(BIGINT,primary_key=True)
#     full_name: Mapped[str] = mapped_column(VARCHAR(255))
#     username: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
#     language_code: Mapped[str] = mapped_column(VARCHAR(10),nullable=False)
#     referrer_id: Mapped[Optional[int]] = mapped_column(BIGINT,ForeignKey('users.telegram_id',ondelete='SET NULL',),nullable=True)

int_pk = Annotated[
    int,
    mapped_column(Integer,primary_key=True, autoincrement=False)
]

str_255 = Annotated[
    str,
    mapped_column(VARCHAR(255))
]

user_fk = Annotated[
    int,
    mapped_column(BIGINT,ForeignKey('users.telegram_id',ondelete='SET NULL'))
]

class User(Base, TimeStampMixin, TableNameMixin):

    telegram_id: Mapped[int_pk]
    full_name: Mapped[str_255]
    user_name: Mapped[Optional[str_255]] 
    language_code: Mapped[str] = mapped_column(VARCHAR(10)) 
    referrer_id: Mapped[Optional[user_fk]]


class Product(Base,TimeStampMixin,TableNameMixin):
    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(3000))
    price: Mapped[float] = mapped_column(DECIMAL(precision=16,scale=4))

class Order(Base,TimeStampMixin,TableNameMixin):
    order_id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(BIGINT,ForeignKey('users.telegram_id',ondelete='CASCADE'))
    user = relationship('User',backref='orders')

class OrderProduct(Base,TableNameMixin):
    order_id: Mapped[int] = mapped_column(Integer,
                                          ForeignKey('orders.order_id',ondelete='CASCADE'),
                                          primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('products.product_id',ondelete='RESTRICT'),
                                            primary_key=True)
    quantity: Mapped[int]

    order = relationship("Order", backref="orderproducts")
    product = relationship("Product", backref="orderproducts")


# # Drops all tables
# Base.metadata.drop_all(engine)

# Creates all tables
# Base.metadata.create_all(engine)