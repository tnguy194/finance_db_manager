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
        (df.exchange=='NASDAQ')) &
        (df.security=='Equity')]

    return df
        

def append_error_csv(ticker: pd.Series):
    df_row = pd.DataFrame(ticker).T
    with open('resources/error.csv', 'a') as file:
        df_row.to_csv(file, header=False)


def setup_error_csv(verify=False):
    if not verify:
        raise ValueError('Set verify=True to reset error csv')
    df = pd.DataFrame([], columns=['name', 'ticker', 'security', 'exchange'])
    with open('resources/error.csv', 'r') as file:
        df.to_csv('error.csv')
