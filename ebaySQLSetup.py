from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy import create_engine
import pymysql
import sqlalchemy.orm
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError
from PrivateInfo import user, password, host, ebay_database


# Establishing a connection to the database
try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{ebay_database}") 
    connection = engine.connect()
    print("Database connection successful")

# Exception handling for any operational errors that might occur during connection
except OperationalError as e:
    print(f"An error occurred: {e}")
    # Handle other operations like logging, cleanup, or retrying here

# Create a base class for the data model using SQLAlchemy's declarative_base
Base = sqlalchemy.orm.declarative_base()

class Brand(Base):
    __tablename__ = 'brand' # Specifying the table name
    id = Column(Integer, primary_key=True) # Primary key column
    name = Column(String(255)) # Brand name column


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    release_date = Column(Date)
    price = Column(Float)

    brand_id = Column(Integer, ForeignKey('brand.id'))

    brand = relationship('Brand', backref='products')
    category = relationship('Category', backref='products')
    product_histories = relationship('Product_History', backref='product')


class Product_History(Base):
    __tablename__ = 'product_history'
    id = Column(Integer, primary_key=True)
    date_listed = Column(Date)
    manufactured_date = Column(Date)
    product_id = Column(Integer, ForeignKey('products.id')) # Foregin key relationship back to product (parent) table
    

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.id'))
    

# Creating tables in Database
Base.metadata.create_all(engine)
