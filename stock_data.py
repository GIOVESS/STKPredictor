# Dependencies for data handling and database operations
import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import engine
from models import StockData
from datetime import datetime

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

# Load stock data from a CSV file
def load_stock_data(filepath, symbol):
    try:
        # Check if stock data for this symbol already exists in the database
        existing_data = session.query(StockData).filter(StockData.stock_symbol == symbol).first()
        
        # If data already exists, skip loading
        if existing_data:
            print(f"Stock data for {symbol} already exists in the database.")
            return

        # If no data exists, proceed with loading the new data
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            # Check if the record already exists in the database for the given date
            existing_record = session.query(StockData).filter(
                StockData.stock_symbol == symbol,
                StockData.date == datetime.strptime(row['Date'], "%Y-%m-%d")
            ).first()

            # If the record already exists, skip adding it
            if not existing_record:
                stock_record = StockData(
                    stock_symbol=symbol,
                    date=datetime.strptime(row['Date'], "%Y-%m-%d"),
                    open_price=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    adj_close=row['Adj Close'],
                    volume=row['Volume']
                )
                session.add(stock_record)

        # Commit all changes to the database
        session.commit()
        print(f"Stock data for {symbol} loaded successfully.")

    except Exception as e:
        print(f"Error loading stock data: {e}")
        session.rollback()

# Fetch stock data for a given symbol
def fetch_stock_data(symbol):
    # Query stock data from the database
    stocks = session.query(StockData).filter_by(stock_symbol=symbol).all()

    if not stocks:
        return None

    # Convert the data to a Pandas DataFrame
    data = {
        "Date": [s.date for s in stocks],
        "Adj Close": [s.adj_close for s in stocks]
    }
    df = pd.DataFrame(data)

    # Ensure the Date column is a datetime object, sort, and set as the index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')  # Sort by date
    df.set_index('Date', inplace=True)

    # Remove duplicate rows based on 'Date'
    df = df[~df.index.duplicated(keep='first')]  # Keep the first occurrence

    # Set frequency of the date index
    df = df.asfreq('B')  # 'B' stands for business days (Monday-Friday)

    return df
