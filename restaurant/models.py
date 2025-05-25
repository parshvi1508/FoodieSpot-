from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cuisine = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    tables = relationship("Table", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100))
    
    reservations = relationship("Reservation", back_populates="user")

class Table(Base):
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    capacity = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    
    restaurant = relationship("Restaurant", back_populates="tables")

class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))
    datetime = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)
    status = Column(String(20), default='confirmed')
    
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")
