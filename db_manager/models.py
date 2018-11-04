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
from sqlalchemy.orm import relationship, backref


base = declarative_base()


class Security(base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)

    def __repr__(self):
        return f'<Security(type={self.type})>'


class Exchange(base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

def __repr__(self):
    return f'<Exchange(type={self.name})>'


class Ticker(base):
    __tablename__ = 'ticker' 
    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String)
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    security_id = Column(Integer, ForeignKey('security.id'))

    exchange = relationship(Exchange, backref='tickers')
    security = relationship(Security, backref='tickers')

    def __repr__(self):
        return f'<Ticker(ticker={self.ticker}, name={self.name}, exchange={self.exchange}, security={self.security})>'


class Price(base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    adj_close = Column(Numeric)
    ticker_id = Column(Integer, ForeignKey('ticker.id'))

    ticker = relationship(Ticker, backref='prices')

    def __repr__(self):
        return f'<Price(date={self.date}, open={self.open}, high={self.high}, low={self.low}, ticker={self.ticker})>'


