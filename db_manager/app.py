# from data_scraper import downloader as dl
# from data_scraper import database as db
import pandas as pd
import params
import file_io as fio
from models import base

import downloader as dl
import database as db


def main():

    mode = input('Mode selection (nodata, update, db_init): ')
    flag_keyboard_interrupt = False
    engine, session = db.connect()
    db_tickers = db.load_available_tickers(session)  # TODO
    new_tickers_df = fio.ticker_list(
        'resources/generic_backup101518.json')
    # TODO remove from list according to error csv
    # TODO remove from list according to db

    if mode == 'nodata':
        start_date = pd.to_datetime(params.START_DATE)
        for ticker in new_tickers_df.iterrows():
            if flag_keyboard_interrupt:
                break
            if ticker['ticker'] not in db_tickers:
                try:
                    data = dl.get_data(ticker, start_date=start_date)
                    db.insert_table(session, data, metadata=ticker)  # TODO
                except KeyboardInterrupt as error:
                    flag_keyboard_interrupt = True
                except Exception:
                    fio.append_error_csv(ticker)  # TODO

    elif mode == 'update':
        for ticker in db_tickers:
            if flag_keyboard_interrupt:
                break
            last_date = db.last_data_date(ticker)
            if last_date < pd.Timestamp.today() - pd.TimeDelta(1, 'D'):
                try:
                    data = dl.get_data(ticker, last_date=last_date)
                    db.insert_table(session, data)  # TODO
                except KeyboardInterrupt as error:
                    flag_keyboard_interrupt = True

    elif mode == 'db_init':
        verify = input('You are about to delete everything '
                       'in the finance_data database (y/n): ')
        if verify == 'y':
            base.metadata.create_all(engine)  # create all tables

    else:
        print('Not a valid mode')


if __name__ == '__main__':
    main()
