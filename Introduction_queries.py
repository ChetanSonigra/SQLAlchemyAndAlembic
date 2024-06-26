from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, create_engine,text
import os,dotenv
dotenv.load_dotenv()

engine = create_engine(
    url=URL.create(
        os.getenv('DRIVER'),
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'),
        os.getenv('HOST'),
        os.getenv('PORT'),
        os.getenv('DB_NAME')
    ),
    echo=True         # to enable logging.
)

session_pool = sessionmaker(engine)

with session_pool() as session:
    # session.execute(text("""

    #     CREATE TABLE users (
    #         telegram_id BIGINT PRIMARY KEY,
    #         full_name VARCHAR(255) NOT NULL,
    #         username VARCHAR(255),
    #         language_code VARCHAR(255) NOT NULL,
    #         created_at TIMESTAMP DEFAULT NOW(),
    #         referrer_id BIGINT,            
    #         FOREIGN KEY(referrer_id)
    #             REFERENCES users(telegram_id)
    #             ON DELETE SET NULL                                 
    #     );
                                  
    #     INSERT INTO users
    #         (telegram_id,full_name,username,language_code,created_at)
    #     VALUES
    #         (1, 'Chetan Sonigra', 'ChetanS','en', '2024-06-26');

    #     INSERT INTO users
    #         (telegram_id,full_name,username,language_code,created_at,referrer_id)
    #     VALUES
    #         (2, 'Chetan Sonigra', 'ChetanSonigra','en', '2024-06-26',1);      
                            
    #     """))
    # session.commit()

    result = session.execute(text('select * from users;'))
    print(result.first())
    # print(result.all())
    # print(result.first())
    # for res in result:
    #     print(res)
    
    result = session.execute(text('select telegram_id from users;'))
    rows = result.scalar()
    print(rows)

    result = session.execute(text('select telegram_id from users;'))
    rows = result.scalars()
    for row in rows:
        print(row)

    # filtering
    result = session.execute(text('select full_name from users where telegram_id= :telegram_id').params(telegram_id=1))
    rows = result.all()
    print(rows)