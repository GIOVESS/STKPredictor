from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from database import Base
# StockData table model
class StockData(Base):
    __tablename__ = "stock_data"
    
    # Define the columns
    stock_id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    
    # Add a unique constraint to ensure no duplicate stock_symbol + date entries
    __table_args__ = (
        UniqueConstraint('stock_symbol', 'date', name='uix_stock_symbol_date'),
    )
    
    def __repr__(self):
        return f"<StockData(symbol='{self.stock_symbol}', date='{self.date}', close={self.close})>"

# User table model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"
