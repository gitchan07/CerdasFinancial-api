from sqlalchemy import create_engine
import os
from sqlalchemy.exc import SQLAlchemyError

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

ENV = os.getenv("ENV_API")

DATABASE_URL = f"myqsl+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

try:
    if ENV == '':
        engine = create_engine(
            DATABASE_URL,
            pool_size=100, 
            max_overflow=50,        
            pool_timeout=100,      
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=True,
        )
    else:
        print("This API uses Production mode")
        engine = create_engine(
            DATABASE_URL,
            max_overflow=40,        
            pool_timeout=10,      
            pool_recycle=180,
            pool_pre_ping=True,pool_use_lifo=True,
        )

    connection = engine.execution_options(isolation_level="READ COMMITTED") 
except SQLAlchemyError as e:
    print(f"An error occurred while connecting to the database: {e}")