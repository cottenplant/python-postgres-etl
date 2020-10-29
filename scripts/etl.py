import json
from typing import OrderedDict
import pandas as pd
import requests
import sys

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError


API_KEY = '03NVr7M8zBFsTJnj0ta2E1K5e0uOvfNGEJg2O4soPiPK5BwuRJMnlfHeZ4NXRH0g'
BASE_URL = 'http://www.zipcodeapi.com/rest/{}/info.json/{}/degrees'
ORDERS_INFILE = Path('./data', 'orders.xlsx')

db_params = {
    'host'      : 'db',
    'database'  : 'challenge',
    'user'      : 'root',
    'password'  : 'password'
}


def db_connect():
    connection = 'postgresql://{user}:{password}@{host}/{database}'\
        .format(**db_params)
    print('connecting to postgresql db ...')
    engine = create_engine(connection)
    return engine


def db_create_seed_table(engine, data_frame, table_name):
    print(f'creating table {table_name}')
    with engine.connect() as conn:
        data_frame.to_sql(
            name=table_name,
            con=conn,
            if_exists='replace',
            index=False
        )


def db_execute_query(engine, sql_query):
    with engine.connect() as conn:
        try: 
            conn.execute(sql_query)
        except ProgrammingError as error:
            print(error, '\ninvalid query')


def get_api_data(zip_code):
    try:
        response = requests.get(BASE_URL.format(API_KEY, zip_code)).text
        payload = json.loads(response)
        return payload
    except requests.exceptions.HTTPError:
        print(f"zip code {zip_code} is invalid")
        return None


def main():
    # initialize db
    engine = db_connect()
    orders_df = pd.read_excel(ORDERS_INFILE, sheet_name='orders.csv')
    db_create_seed_table(engine, orders_df, 'orders')
    
    # extract and load data from api
    zip_codes = set(orders_df['zipcode'].values)
    zip_codes_loc = [get_api_data(zip_code) for zip_code in zip_codes]
    zip_codes_loc_df = pd.DataFrame(zip_codes_loc)[['zip_code', 'lat', 'lng', 'city', 'state']]
    db_create_seed_table(engine, zip_codes_loc_df, 'zip_codes_loc')

    # update database

    engine.dispose()


if __name__ == '__main__':
    main()
