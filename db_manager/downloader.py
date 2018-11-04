import pandas as pd
import pandas_datareader as web


def get_data(ticker, start_date=None, last_date=None):
    """
    Returns data retrieved from yahoo finance.
    Has 2 modes depending on which parameter is passed
        start_date - download from start_date until today - 1
        last_date - download data starting from last_date + 1
    """
    if (start_date is not None) ^ (last_date is not None):
        reader_end_date = pd.Timestamp.now() - pd.Timedelta(1, 'D')

        if start_date is not None:  # ticker not in db
            data = web.DataReader(ticker, data_source='yahoo',
                                  start=start_date, end=reader_end_date)
        elif last_date:  # ticker in db, only updating to newest daily close
            start_date = last_date + pd.Timedelta(1, 'D')
            data = web.DataReader(ticker, data_source='yahoo',
                                  start=start_date, end=reader_end_date)

        data.reset_index(inplace=True)
        data.columns = ['date', 'high', 'low', 'open',
                        'close', 'volume', 'adj_close']
        return data
    else:
        raise ValueError("start_date and last_date are mutally exclustive")
