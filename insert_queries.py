from table_creation import User
from sqlalchemy.orm import Session
from sqlalchemy import insert

# Repository is a class that stores and manages database interactions.

class Repo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_user(self,telegram_id: int, full_name: str,language_code: str, username: str = None,referrer_id: int = None):
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

        stmt = insert(User).values(
            telegram_id=telegram_id,
            full_name=full_name,
            user_name=username,
            language_code=language_code,
            referrer_id=referrer_id
        )
        print(stmt)
        self.session.execute(stmt)
        self.session.commit()


if __name__=="__main__":
    from database_connection import session_pool
    with session_pool() as session:
        repo = Repo(session)
        repo.add_user(
            telegram_id=2,
            full_name="Chetan Gajjar",
            language_code='en',
            username='ChetanG'
        )