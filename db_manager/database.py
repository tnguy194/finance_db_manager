import params
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Ticker, Price, Security, Exchange
import utils


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


@utils.my_timer
def insert_data(session, data, metadata):
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
        print('No metadata')
    else:  # new data

        exchange = Exchange(name=metadata['exchange'])
        security = Security(type=metadata['security'])
        mapped_ticker = Ticker(ticker=metadata['ticker'],
                               name=metadata['name'],
                               exchange=exchange,
                               security=security)  # TODO create a mapping object
        data = data.to_dict(orient='records')  # list of dicts

        # print('Debugging - mapped_ticker')  # debugging
        # print(mapped_ticker)  # debugging

        # print('Debugging - Data length')  # debugging
        # print(len(data))  # debugging
        # print('Debugging - Data')  # debugging
        # print(data)
        
        price_list = list()
        for item in data:  # merge metadata to data
            date = item['date']
            high = item['high']
            low = item['low']
            open = item['open']
            close = item['close']
            volume = item['volume']
            adj_close = item['adj_close']

            # data_point = Price(date=date,
            #                    open=open,
            #                    high=high,
            #                    low=low,
            #                    close=close,
            #                    adj_close=adj_close,
            #                    ticker=mapped_ticker)

            data_point = {'date': date, 'open': open, 'high': high,
                          'low': low, 'close': close, 'adj_close': adj_close,
                          'ticker': mapped_ticker}

            price_list.append(data_point)

            # print('Debugging - printing data_point')  # debugging
            # print(data_point)  # debugging

        # print('Debugging - price_list')  # debugging 
        # print(price_list)  # debugging

        # print(f'Inserting data into DB')  # debugging
        session.bulk_insert_mappings(Price, price_list)
        # print(f'Data inserted')  # debugging

        # TODO create relations, as it stands, only price data are inserted,
        # TODO not any of the metadata
        # TODO data mapping is incorrect
