from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Create SQLite database
engine = create_engine('sqlite:///restaurant_reservations.db', echo=True)

# Create all tables
Base.metadata.create_all(engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

print("Database created successfully!")
