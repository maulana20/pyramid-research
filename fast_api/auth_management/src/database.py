from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="mysql+mysqlconnector",
    username="safous",
    password="safous",
    host="db",
    database="safous_auth",
    port=3306
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()