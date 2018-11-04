import params
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Ticker


def connect():
    """
    Connect to SQL database as specified by params.DBSTRING
    """
    engine = create_engine(params.DB_STRING)
    Session = sessionmaker(engine)
    session = Session()
    return engine, session


def data_in_db():
    pass


def load_available_tickers(session):
    """
    Get a list of all tickers in db
    """
    # tickers = session.query(Ticker.ticker).all()
    # return tickers
    pass

def insert_data(session, data, metadata=None):
    """
    Insert data into db
    :param data: df with columns
        date
        high
        low
        open
        close
        volume
        ajd_close
    :param metadata: df with single row
        name
        ticker
        security
        exchange
    """
    if not metadata:  # updating
        pass
    else:  # new data
        pass    
        
        company_ticker = Ticker(ticker=metadata['ticker'],
                                name=metadata['name'])
