import pandas as pd


def ticker_list(path: str):
    """
    Load and reformat tickers
    """
    tickers = pd.read_json(path)
    tickers = tickers[['Name', 'Ticker', 'TypeDisplay', 'exchangeDisplay']]
    tickers.columns = ['name', 'ticker', 'security', 'exchange']
    return tickers

def us_equities(path: str):
    """
    Filter out all non-US equities
    """
    df = ticker_list(path)

    df = df[(
        (df.exchange=='NYSE') |
        (df.exchange=='NYSEArca') |
        (df.exchange=='NASDAQ') | 
        (df.exchange=='NYSE MKT')) &
            (df.security=='Equity')]
