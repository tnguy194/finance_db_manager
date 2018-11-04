"""
Relationship mapping
    Ticker
        relationship to Price
        foreign key to Exchange
        foreign key to Security
    Price
        foreign key to Ticker
    Exchange
        relationship to Ticker
    Security
        relationship to Ticker
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship


base = declarative_base()


class Price(base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    ticker_id = Column(Integer, ForeignKey('ticker.id'))  # column constraint

    # def __init__(self, date, open, high, low, ticker):
    #     self.date = date
    #     self.open = open
    #     self.high = high
    #     self.low = low


class Ticker(base):
    __tablename__ = 'ticker'

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True)
    name = Column(String)
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    security_id = Column(Integer, ForeignKey('security.id'))

    # exchange = relationship('Exchange')
    # security = relationship('Security')
    prices = relationship('Price', back_populates='ticker')

    # def __init__(self, ticker, name):
    #     self.ticker = ticker
    #     self.name = name


class Security(base):
    __tablename__ = 'security'

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)

    tickers = relationship('Ticker', back_populates='security')

    # def __init__(self, type):
    #     self.type = type


class Exchange(base):
    __tablename__ = 'exchange'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    tickers = relationship('Ticker', back_populates='security')

    # def __init__(self, name):
    #     self.name = name
