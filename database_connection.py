from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import psycopg2
import dotenv, os

dotenv.load_dotenv()


#  docker run --name postgresql -e POSTGRES_PASSWORD=testpassword -p 5432:5432 -d postgres:latest  

# Connection String Format: driver+postgresql://user:pass@host:port/dbname
url = URL.create(os.getenv('DRIVER'),
                 os.getenv('POSTGRES_USER'),
                 os.getenv('POSTGRES_PASSWORD'),
                 os.getenv('HOST'),
                 os.getenv('PORT'),
                 os.getenv('DB_NAME'))
engine = create_engine(url) # pool_recyle, pool_size, max_overflow parameters.
# print(url.render_as_string(hide_password=False))

session_pool = sessionmaker(engine)

# session = session_pool()
# or 

with session_pool() as session:
    result = session.execute(text('SELECT 1'))
    print(result.fetchone())
