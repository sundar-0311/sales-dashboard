import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

engine = create_engine('sqlite:///my_database.db')

logging.basicConfig(
  filename= "logs/data_insertion.log",
  level=logging.INFO,
  format= '%(asctime)s:%(levelname)s:%(message)s',
  filemode= 'a'
)

def insert_data(df, table_name, engine):
  df.to_sql(table_name, con=engine, if_exists='replace', index=False) 
  # if the table already exists, it will be replaced with the new data.
  # index=False means that the DataFrame index will not be written to the database table.

def load_raw_data():
  start_time = time.time()
  for file in os.listdir('data'):
    if file.endswith('.csv'):
      df= pd.read_csv('data/' + file)
      logging.info(f'ingesting file: {file} with shape: {df.shape}') 
      insert_data(df, file[:-4], engine) # file[:-4] removes the .csv extension from the filename to use as the table name in the database.
  end_time = time.time()
  total_time = (end_time - start_time) / 60
  logging.info('ingestion completed')
  logging.info(f'Total time taken for data insertion: {total_time:.2f} minutes')

if __name__ == "__main__":
  load_raw_data()