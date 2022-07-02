#TO CONNECT TO THE DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#above imports copied from fastAPI/alchemy
from .config import settings #import the initiated setting here to import secret vals


#connection to DB for queries - Unique URL to connect to DB: format: SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:password@<ip_address/hostname>/<db_name>'

#with config.py file
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


#engine to connect alchemy to postgres for queries
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session for talking to DB
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

#create dependancy, this func get a connection/session to DB when we get a request, sends a sql statement to it, closes after the request is done.
def get_db(): #copied from fast api/alchemy
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
