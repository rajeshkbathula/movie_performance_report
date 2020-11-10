import pandas as pd
import os
from sqlalchemy import create_engine
from config import *


def postgres_connect(user='db_admin',passwd='db_admin',db='movie_database'):
    """
    postgres connection using psycopg2 module
    :param user: str :usename
            passwd :  str : password
            db : str : database
    :return: Bool true or false
    """
    try:
        logger.info(f"Establishing Postgres connection !")
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
    logger.info(f"Feeding data into postgres Table!")
    if not connection:
        connection = postgres_connect()
    try:
         pandas_df.to_sql(table, connection)
    except ValueError as vx:
        logger.Warning(f"Postgres Warning to ValueError with exception  {vx} , Droping and Recreating! ")
        try:
            db = db_connect()
            db.execute(
                f"DROP TABLE IF EXISTS {postgres_table_name_wiki}")
            pandas_df.to_sql(table, connection)
        except ValueError as vx:
            logger.error(f"Postgres connection Failed With Exception {vx}!")
        except Exception as ex:
            logger.error(f"Postgres connection Failed With Exception {ex}")
    except Exception as ex:
        logger.error(f"Postgres connection Failed With Exception {ex}")
    else:
        logger.info(f"Postgres Table {table} has been created successfully.")
    finally:
        connection.close()
        return True


def db_connect():
    """
    db conect workaround
    :param connection: 
    :return: class
    """
    return create_engine(create_engine("postgresql://db_admin:db_admin@localhost:5432/movie_database"))

def postgres_view_with_final_results(connection=None,db=None):
    """
    this function will create view in wiki and metedata to offer links
    :param connection: connection :postgres connection
            table :  str : table name
            pandas_df : DataFrame
    :return: Bool true or false
    """
    try:
        db = db_connect()
        query = f" CREATE OR REPLACE VIEW {top_ratio_movies_view_name} AS SELECT a.title as tile,rating as rating, budget as budget, \
            year as year,revenue as revenue, ratio as ratio, companies as production_companies, \
             link as link, abstact as abstract FROM {postgres_table_name_movies} a join {postgres_table_name_wiki} b on a.title = b.title order by ratio,year,revenue"
        db.execute(query)
    except ValueError as vx:
        logger.error(f"Postgres connection Failed With Exception {vx}!")
    except Exception as ex:
        logger.error(f"Postgres connection Failed With Exception {ex}")
    else:
        logger.info(f"Postgres Table {top_ratio_movies_view_name} has been created successfully.")
    finally:
        connection.close()
