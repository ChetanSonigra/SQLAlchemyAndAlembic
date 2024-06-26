from table_creation import User
from sqlalchemy.orm import Session
from sqlalchemy import insert,select, or_

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