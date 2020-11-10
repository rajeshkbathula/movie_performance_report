import logging
import logging_loki

handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"movie_database": "top_revenue_movies"},
    # auth=("username", "password"),
    version="1",
)

logger = logging.getLogger("top_revenue_movies_python_script")
logger.addHandler(handler)

wiki_df_columns = ['title','link','abstract']

raw_csv_columns = ['title','budget','release_date','revenue','vote_average','vote_average','production_companies']

csv_filtered_columns = {'budget':'int','genres':'string','title':'string','companies':'string',
                                  'release_date':'string','revenue':'int','rating':'float'}

postgres_table_name_movies = 'movie_metadata'

postgres_table_name_wiki = 'wiki_link'

table_name_raw_movies_meta = 'raw_movie_metadata'

grafana_link = None

final_table_query_link = "http://localhost:9000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22postgres%22,%7B%22datasource%22:%22postgres%22,%22format%22:%22time_series%22,%22timeColumn%22:%22time%22,%22metricColumn%22:%22none%22,%22group%22:%5B%5D,%22where%22:%5B%7B%22type%22:%22macro%22,%22name%22:%22$__timeFilter%22,%22params%22:%5B%5D%7D%5D,%22select%22:%5B%5B%7B%22type%22:%22column%22,%22params%22:%5B%22value%22%5D%7D%5D%5D,%22rawQuery%22:false%7D%5D"
