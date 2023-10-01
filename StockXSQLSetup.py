# Import necessary modules from SQLAlchemy, PyMySQL, and urllib.parse
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
import pymysql
import sqlalchemy.orm
from sqlalchemy.exc import OperationalError


# Importing Private Database Information:
from PrivateInfo import user, password, host, stockx_database

# Establishing a connection to the database
try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{stockx_database}") 
    connection = engine.connect()
    print("Database connection successful")

# Exception handling for any operational errors that might occur during connection
except OperationalError as e:
    print(f"An error occurred: {e}")
    # Handle other operations like logging, cleanup, or retrying here

# Create a base class for the data model using SQLAlchemy's declarative_base
Base = sqlalchemy.orm.declarative_base()

# Product Info class inhereits from base class
class Product_Info(Base):
    __tablename__ = 'Product_Info'
    id = Column(Integer, primary_key=True)
    product_line = Column(String(255))
    release_date = Column(String(255))
    retail_price = Column(Float)
    product_name = Column(String(255))
    resale_price = Column(Float)

# Creating tables in Database
Base.metadata.create_all(engine)

