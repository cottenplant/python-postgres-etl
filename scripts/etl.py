import json
import os
import pandas as pd
import requests

from sqlalchemy import create_engine
from sqlalchemy import engine


ORDERS_FILE = 'data/orders.xlsx'
BASE_URL = 'http://www.zipcodeapi.com/rest/' \
           'SJ5Z7T6wru3SpYMGiG8mDrTgq4mbKLgllmrbmaf9AXhJghx92GX4LnFZ102Y6DHk/info.json/{zip_code}/degrees'


def connect_to_db():
    conn_str = "postgresql+psycopg2://root:password@db:5432/challenge"
    engine = create_engine(conn_str)
    
    return engine
    
    
def write_to_db(data_frame, engine):
    with engine.connect() as conn:
        data_frame.to_sql(data_frame, conn)


def get_zip_codes():
    pass


def get_api_data(zip_codes):
    for zip_code in zip_codes:
        try:
            response = requests.get(BASE_URL.format(zip_code)).text
            payload = json.loads(response)
            return payload

        except requests.exceptions.HTTPError:
            print(f"zip code {zip_code} is invalid")

    

def main():
    orders_df = pd.read_excel(ORDERS_FILE, sheet_name='orders.csv')
    engine = connect_to_db()
    write_to_db(orders_df, engine)



if __name__ == '__main__':
    main()
