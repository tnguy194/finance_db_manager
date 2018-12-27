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
    # db_tickers = db.load_available_tickers(session)  # TODO
    db_tickers = []  # testing
    new_tickers_df = fio.us_equities(
        'resources/generic_backup101518.json')
    # TODO remove from list according to error csv
    # TODO remove from list according to db

    if mode == 'nodata':
        start_date = pd.to_datetime(params.START_DATE)
        for ticker_row in new_tickers_df.iterrows():  # looping over all tickers
            ticker_row = ticker_row[1]  # get rid of the indexing
            metadata = ticker_row.to_dict()

            print('Debugging - printing metadata')  # debugging
            print(metadata)  # debugging

            if flag_keyboard_interrupt:  # interruption logic
                print('Keyboard interrupted - exiting...')
                break

            if ticker_row['ticker'] not in db_tickers:  # skip over existing tickers
                try:
                    data = dl.get_data(ticker_row['ticker'],
                                       start_date=start_date)

                    print(f"Inserting {ticker_row['ticker']} into db")  # debugging

                    db.insert_data(session, data, metadata=metadata)
                    session.commit()

                except KeyboardInterrupt as error:
                    flag_keyboard_interrupt = True
                # except Exception:  # can't debug if errors don't show
                #     fio.append_error_csv(ticker_row)  # TODO


    elif mode == 'update':
        for ticker in db_tickers:
            if flag_keyboard_interrupt:  # ctrl-c break
                break
            last_date = db.last_data_date(ticker)  # TODO
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
        fio.setup_error_csv(verify=True)

    else:
        print('Not a valid mode')


if __name__ == '__main__':
    main()
