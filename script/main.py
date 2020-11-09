"""
Python script that reads opensource movies metadata filter
required fileds by mapping it to IMDB wiki file
"""
import gzip
import re
import pandas as pd
import csv
from zipfile import ZipFile
import datetime
from config import *
from postgres_feed_data import *

def filter_profit_movies(df,budget_limit_above=None):
    """
    this function will return pandas dataframe after filtering input dataframe
    revenue greater than budget and adding filter to avoid below 0 budget movies
    :param DataFrame
    :return: DataFrame
    """
    if not budget_limit_above:
        budget_limit_above = min_budget_limit
    df['budget'] = df['budget'].apply(pd.to_numeric)
    df =  df[(df['budget'] > budget_limit_above) & (df['revenue'] > df['budget'])]
    return df

def extract_year_from_release_date(df):
    """
    this function will return pandas dataframe
    :param DataFrame
    :return: DataFrame
    """
    df['year'] = pd.DatetimeIndex(df['release_date']).year
    return df

def calc_ratio_from_budget_and_revenue_filter_top_once(df,num=None):
    """
    this function will return pandas dataframe by taking dataframe as input and calculating ration
    budget/revenue on those columns and adding ratio column to df
    :param DataFrame : dataframe with movies data in it
    :return: DataFrame : dataframe with ratio
    """
    if not num:
        num = top
    df = df.fillna(0)
    # df['ratio'] = df['budget'] / df['revenue']
    df['ratio'] = df['revenue'] / df['budget']
    df.sort_values(by=['ratio'], inplace=True, ascending=False)
    df = df.head(num).reset_index(drop=True)
    return df

def unzip_wiki_file(source_filepath, block_size=65536):
    """
    this function will unzips gzip'ed file and places it in same directory after decrompression
    :param source_filepath: str
    :return: str
    """
    try:
        dest_dirpath = os.path.dirname(source_filepath)
        file_basename = os.path.basename(source_filepath)
        xml_decompressed_path = f"{dest_dirpath}/{file_basename.split('.')[0]}.xml"
        logger.info(f"XML unzipping in progress!")
        with gzip.open(source_filepath, 'rb') as s_file, \
            open(xml_decompressed_path, 'wb') as d_file:
            while True:
                block = s_file.read(block_size)
                if not block:
                    return xml_decompressed_path
                else:
                    d_file.write(block)
                    logger.debug(f"XML unzipping in progress!")
    except Exception as e:
        logger.error(f"decompress failed for file [{source_filepath}] with excception {e} stoping process!")
        quit()

def extract_wiki_xml_into_pandas_df(xml_file_path, movie_df,num = None):
    """
    this function will return pandas dataframe
    :param xml_file: file path
            df : dataframe
    :return: DataFrame
    """
    if not num:
        num = top
    dest_dirpath = os.path.dirname(xml_file_path)
    file_basename = os.path.basename(xml_file_path)
    xml_filter_file_path = f"{dest_dirpath}/{file_basename.split('.')[0]}_work.xml"
    logger.debug(f"xml file name {xml_file_path}")
    wiki_filter_list = []
    logger.info(f"XML wiki extract for columns in progress!")
    cnt = 0
    top_movie_titles = tuple(movie_df.title.tolist())
    with open(xml_file_path, "r") as file,  open(xml_filter_file_path,'w') as wiki_file:
        writer = csv.writer(wiki_file)
        writer.writerow((item for item in wiki_df_columns))
        for line in file:
            logger.debug(f"XML wiki extract for columns in progress found {len(wiki_filter_list)} out of [{num}]")
            logger.debug(f"xml file name {line}")
            title = link = abstract = None
            try:
                if line.startswith("<title>"):
                    title = re.findall(r'<title>Wikipedia: (.*?)</title>', line)[0]
                    link = re.findall(r'<url>(.*?)</url>', next(file))[0]
                    abstract = re.findall(r'<abstract>(.*?)</abstract>', next(file))
                    if title and title in top_movie_titles :
                        cnt += 1
                        writer.writerow((title,link,abstract))
                        logger.info(f"Running Matched with top : [{cnt}] from movies : [{num}]")
                        if cnt == num:
                            logger.info(f"Matched with top : [{cnt}]  from movies  : [{num}]")
                            return xml_filter_file_path
                    else:
                        logger.debug(f"title not in movie list!")
            except Exception as e:
                logger.error(f"xml parsing into dataframe failed with Ecxception {e} !")
                quit()
    logger.info(f"Matched with top : [{cnt}]  from movies : [{num}]")
    return xml_filter_file_path

def string_ascii_check(string):
    """
    this function will check ascii ar no passes string argument and returns string if its asci if not None
    :param string:  str
    :return:  str or None
    """
    return re.sub(r'[^\x00-\x7f]',r'', string)

def filter_bad_records(file_path : str):
    """
    this function will filter bad records from CSV on if not asci or they don't have enough column
    or wrong datatype in budget and revenue
    :param csv_files_list:  file paths location
    :return:  location file path that has csv data filteres
    """
    try:
        dest_dirpath = os.path.dirname(file_path)
        with ZipFile(file_path, 'r') as zipObj:
            zipObj.extractall(dest_dirpath)
        file = f'{file_path.rsplit(".", 1)[0]}'
        work_file = f'{file_path.rsplit(".", 1)[0]}.work'
        with open(file, 'r') as inp, open(work_file, 'w') as out:
            writer = csv.writer(out)
            writer.writerow(csv_filtered_columns.keys())
            logger.info(f"Movies csv extract in progress!")
            for row in csv.reader(inp):
                title = string_ascii_check(row[8])
                if title and len(row) == 24 and str.isnumeric(row[2]) and str.isnumeric(row[15]):
                    row = row[2], row[3], row[8], row[12], row[14], row[15], row[22]
                    writer.writerow(row)
                    logger.debug(f"Movies csv extract in progress!")
                elif len(row) == 24:
                    logger.debug(f"row not good to proceed with error key columns : [{row}] !")
                else:
                    logger.debug(f"row not good to proceed with no of columns ae not matching : [{row}] !")
        return work_file
    except Exception as e:
        logger.error(f"filtering bad recirds failed with Ecxception {e} !")
        quit()

def extract_metadata_csv_into_pandas_df(csv_files_path : str):
    """
    this function will return pandas dataframe after loading csv file path argument
    :param csv_files_list:  file paths location
    :return: DataFrame
    """
    try:
        return pd.read_csv(csv_files_path,dtype=csv_filtered_columns)
    except Exception as e:
        logger.error(f"csv parsing into dataframe failed with Ecxception {e} !")
        quit()

def time_now():
    '''
        This function will retun time now in HHMMSS format
        '''
    return int(datetime.datetime.now().strftime('%H%M%S'))

def main(xml_file_path,csv_file_path):
    '''
    This function is the starting point that calls other functions
            that does filter adn do other jobs
        Parameters:
            None

        Returns:
            value (bool): True or False
    '''
    start_time = time_now
    logger.info("main function called!")
    filtered_csv_records_file = filter_bad_records(csv_file_path)
    movie_metedata_df = extract_metadata_csv_into_pandas_df(filtered_csv_records_file)
    profit_movies_df = filter_profit_movies(movie_metedata_df)
    top_ratio_movies = calc_ratio_from_budget_and_revenue_filter_top_once(profit_movies_df)
    movies_with_year_df = extract_year_from_release_date(top_ratio_movies)
    pandas_to_postgres_table(postgres_table_name_movies,movies_with_year_df)
    movie_time = time_now
    logger.info(f"wiki CSV load to postgres done  {round(float((movie_time - start_time)/60), 2)} Mins!")

    xml_file_decompressed_path = unzip_wiki_file(xml_file_path)
    wiki_list_filtered_to_match_movies = extract_wiki_xml_into_pandas_df(xml_file_decompressed_path,movies_with_year_df)
    wiki_final_df = pd.DataFrame(wiki_list_filtered_to_match_movies)
    postgres_table_name_wiki(postgres_table_name_wiki,wiki_final_df)
    wiki_time = time_now
    logger.info(f"wiki CSV load to postgres done  {round(float((wiki_time - movie_time) / 60), 2)} Mins!")
    end_time = time_now
    logger.info(f"main function Ended took {round(float((end_time - start_time)/60),2)} Mins!")

if __name__ == '__main__':
    top = 2
    min_budget_limit = 1000
    main('./data/enwiki-latest-abstract.xml.gz','./data/movies_metadata.csv.zip')
    
