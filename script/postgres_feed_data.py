import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from config import *

def postgres_connect(user='db_user',passwd='db_user',db='movie_database'):
    """
    postgres connection using psycopg2 module
    :param user: str :usename
            passwd :  str : password
            db : str : database
    :return: Bool true or false
    """
    try:
        alchemyEngine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@localhost/{db}',
                                      pool_recycle=3600)
        postgreSQLConnection = alchemyEngine.connect()
    except Exception as e:
        logger.error(f"Postgres connection Failed to DB {db} with exception {e}")
    else:
        logger.info(f"Postgres DB connection successful to DB :  {db} has been created")
        return postgreSQLConnection

def pandas_to_postgres_table(table,pandas_df,connection=None):
    """
    this function will inject data from Pandas DF into Postgres
    :param connection: connection :postgres connection
            table :  str : table name
            pandas_df : DataFrame
    :return: Bool true or false
    """
    if not connection:
        connection = postgres_connect()
    try:
        pandas_df.to_sql(table, connection)
    except ValueError as vx:
        logger.error(f"Postgres connection Failed to ValueError with exception  {vx}")
    except Exception as ex:
        logger.error(f"Postgres connection Failed With Exception {ex}")
    else:
        logger.info(f"Postgres Table {table} has been created successfully.")
    finally:
        connection.close()
        return True

def postgres_view_with_final_results(connection, table,pandas_df):
    """
    this function will inject data from Pandas DF into Postgres
    :param connection: connection :postgres connection
            table :  str : table name
            pandas_df : DataFrame
    :return: Bool true or false
    """
    pass