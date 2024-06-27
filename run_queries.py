from table_creation import User, Order, Product, OrderProduct
from sqlalchemy.orm import Session
from sqlalchemy import insert,select, or_
from sqlalchemy.dialects.postgresql import insert as postgres_insert
import random

# Repository is a class that stores and manages database interactions.

class Repo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_user(self,telegram_id: int, full_name: str,language_code: str, username: str = None,referrer_id: int = None) -> User:
        # user = User(
        #     telegram_id=telegram_id,
        #     full_name=full_name,
        #     language_code=language_code,
        #     user_name=username
        # )
        # self.session.add(user)
        # self.session.commit()
        # return user

        # or

        stmt = select(User).from_statement(
            insert(User).values(
            telegram_id=telegram_id,
            full_name=full_name,
            user_name=username,
            language_code=language_code,
            referrer_id=referrer_id
        ).returning(
            User
            )
        )
        print(stmt)
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()

    def add_order(self, user_id: int) -> Order:
        stmt = select(Order).from_statement(insert(Order).values(user_id=user_id).returning(Order))
        result = self.session.scalars(stmt)
        return result.first()

    def add_product(self, title: str, description: str, price: float) -> Product:
        stmt = select(Product).from_statement(
            insert(Product).values(title=title, description=description, price=price).returning(Product)
        )
        result = self.session.scalars(stmt)
        return result.first()

    def add_order_to_product(self,order_id: int, product_id: int,quantity: int):
        stmt = (insert(OrderProduct).values(order_id=order_id,product_id=product_id,quantity=quantity))

        result = self.session.execute(stmt)
        self.session.commit()

    def get_user_by_id(self,telegram_id: int) -> User:
        # user = self.session.query(User).filter(User.telegram_id==telegram_id).first()
        # return user
       
        # or

        stmt = select(User).where(User.telegram_id==telegram_id)
        print(stmt)
        result = self.session.execute(stmt)
        return result.scalars().first()
    
    def get_all(self):
        stmt = select(
                User
            ).where(
                User.full_name.like('%jj%'),  
                or_(User.language_code == 'en',User.language_code == 'uk')
            ).group_by(
                User.telegram_id
            ).having(
                User.telegram_id>0
            ).order_by(
                User.created_at.desc()
            ).limit(
                5
            )
        result = self.session.execute(stmt)
        return result.scalars().all()

    def get_user_language(self,telegram_id: int) -> str:
        stmt = select(User.language_code).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        return result.scalar()

    def everything(self,telegram_id: int, full_name: str,language_code: str, username: str = None,referrer_id: int = None):
        stmt = select(User).from_statement(
            postgres_insert(User)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                user_name=username,
                language_code=language_code,
                referrer_id=referrer_id
            )
            .returning(
                User
            )
            .on_conflict_do_update(
                index_elements = [User.telegram_id],
                set_=dict(
                    user_name=username,
                    full_name=full_name
                )
            )
        )
        result = self.session.scalars(stmt).first()
        self.session.commit()
        return result

from faker import Faker    
def seed_fake_data(repo: Repo):
    Faker.seed(40)
    fake = Faker()
    users: list[User]= []
    products: list[Product]= []
    orders: list[Order]= []

    for _ in range(8):
        referrer_id = None
        print(users)
        if len(users)>=1:
            print(users[-1])
            referrer_id = users[-1].telegram_id
        user = repo.add_user(
            telegram_id=fake.pyint(),
            full_name=fake.name(),
            username=fake.user_name(),
            language_code=fake.language_code(),
            referrer_id=referrer_id
        )

        users.append(user)

    for _ in range(10):
        order = repo.add_order(
            user_id= random.choice(users).telegram_id
            )
        orders.append(order)

    for _ in range(10):
        product = repo.add_product(
            title=fake.word(),
            description=fake.sentence(),
            price=fake.pyint()
            )
        products.append(product)

    for order in orders:
        for _ in range(2):
            repo.add_order_to_product(
                order_id=order.order_id,
                product_id=random.choice(products).product_id,
                quantity=random.randint(1,20)
                )




if __name__=="__main__":
    from database_connection import session_pool
    with session_pool() as session:
        repo = Repo(session)
        # repo.add_user(
        #     telegram_id=2,
        #     full_name="Chetan Gajjar",
        #     language_code='en',
        #     username='ChetanG'
        # )

        user = repo.get_user_by_id(1)
        print(user.telegram_id,user.full_name,user.user_name,user.language_code)
        users = repo.get_all()
        print(users)
        lang = repo.get_user_language(1)
        print(lang)
        user = repo.everything(2,'Chetan M Gajjar','en','ChetanGajjar')
        print(user)

        seed_fake_data(repo)