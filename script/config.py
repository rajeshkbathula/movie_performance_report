import os
import logging
import sys
from pythonjsonlogger import jsonlogger


logger_name = os.environ.get('logger_name', 'local')
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(levelname)s - %(asctime)s  - %(message)s - %(name)s - %(lineno)d - %(filename)s ')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate=False
logger.setLevel(logging.INFO)


wiki_df_columns = ['title','link','abstract']

raw_csv_columns = ['title','budget','release_date','revenue','vote_average','vote_average','production_companies']

csv_filtered_columns = {'budget':'int','genres':'string','title':'string','companies':'string',
                                  'release_date':'string','revenue':'int','rating':'float'}

postgres_table_name_movies = 'movie_metadata'

postgres_table_name_wiki = 'movie_metadata'

grafana_link = None

dashboard_link = None
