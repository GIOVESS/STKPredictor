# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ensure the db directory exists
db_dir = "E:/PYTHON PROJECTS/STKpredictor/db/"
os.makedirs(db_dir, exist_ok=True)

# SQLAlchemy setup
Base = declarative_base()

# Use the absolute path to the database
db_path = f"sqlite:///{os.path.join(db_dir, 'stock_predictor.db')}"

# Create the engine with the correct database path
engine = create_engine(db_path, echo=True)

Session = sessionmaker(bind=engine)

# Initialize database tables (for StockData, User, etc.)
def init_db():
    # Import models to ensure tables are created
    from models import User,StockData  # Import the User model

    # Create all tables defined in models (this includes StockData and User)
    Base.metadata.create_all(engine)

    # Print the path where the database is created
    print(f"Database tables created at: {os.path.abspath(db_path)}")
