"""
Python script that reads opensource movies metadata filter
required fileds by mapping it to IMDB wiki file
"""
import gzip
import glob
import logging
import sys
import os, re
from pythonjsonlogger import jsonlogger
import pandas as pd
from schema_config import *

logger_name = os.environ.get('logger_name', 'local')
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(name)s - %(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate=False
logger.setLevel(logging.INFO)

# print(self.raw_wiki_abstract_df.info())
# print(self.raw_wiki_abstract_df[['title', 'links']], self.raw_movies_metadata_csv_df['title'])
# sc = list(map(lambda st: str.replace(st, raw_xml_flatten_columns[-1], "link"), raw_xml_flatten_columns))
# df = pd.DataFrame(columns=sc)
# df[sc] = self.wiki_abstract_flatten_df[raw_xml_flatten_columns]
# print(df.head())


def decompress_wiki_xml_file(source_filepath: str) -> list:
    """
    this function will return pandas dataframe
    :param location: location of input files
    :return: list
    """
    try:
        src_xml_gz_files = glob.glob("{}/*.gz".format(source_filepath))
        if len(src_xml_gz_files) > 0:
            for file in src_xml_gz_files:
                unzip_wiki_file(file)
        src_xml_files = glob.glob("{}/*.xml".format(source_filepath))
        if len(src_xml_files) > 0:
            return src_xml_files
        else:
            logger.error('No xml wiki files in input folder, kindly upload and rerun from project folder!')
            sys.exit()
    except Exception as e:
        print("kindly place xml files in data folder and try again!")

def unzip_wiki_file(source_filepath, block_size=65536):
    try:
        dest_dirpath = os.path.dirname(source_filepath)
        file_basename = os.path.basename(source_filepath)
        with gzip.open(source_filepath, 'rb') as s_file, \
            open(f"{dest_dirpath}/{file_basename.split('.')[0]}.xml", 'wb') as d_file:
            while True:
                block = s_file.read(block_size)
                if not block:
                    return
                else:
                    d_file.write(block)
    except Exception as e:
        logger.error(f"decompress failed for file [{source_filepath}] with excception {e} stoping process!")
        raise

# df = read_xml_to_df('./data')
# df.info()

# def extract_wiki_xml_into_pandas_df(xml_files_list : list):
#     """
#     this function will return pandas dataframe
#     :param xml_files_list: list with file paths
#     :return: DataFrame
#     """
#     df = pd.DataFrame(columns=wiki_df_columns)
#     for file in xml_files_list:
#         with open(file, "r") as xml_file:
#             for line in xml_file:
#                 if line.startswith("<title>"):
#                     df.loc[len(df.index)] = [re.findall(r'>(.*?)<', line)[0].strip('Wikipedia: '), re.findall(r'>(.*?)<', next(xml_file))[0],
#                                              re.findall(r'>(.*?)<', next(xml_file))]
#                     print(df.info())
#     print(df.info())

def extract_wiki_xml_into_pandas_df(xml_files_list : list):
    """
    this function will return pandas dataframe
    :param xml_files_list: list with file paths
    :return: DataFrame
    """
    df = pd.DataFrame(columns=wiki_df_columns)
    for file in xml_files_list:
        with open(file, "r") as xml_file:
            for line in xml_file:
                title = link = abstract = None
                try:
                    if line.startswith("<title>"):
                        title = re.findall(r'>(.*?)<', line)[0].strip('Wikipedia: ')
                        link = re.findall(r'>(.*?)<', next(xml_file))[0]
                        abstract = re.findall(r'>(.*?)<', next(xml_file))
                    if title:
                        df.loc[len(df.index)] = [title,link,abstract]
                        
                except Exception as e:
                    logger.error(f"xml parsing into dataframe failed with Ecxception {e} !")
                    quit()
    
    return df




def extract_metadata_csv_into_pandas_df(csv_files_path : str):
    """
    this function will return pandas dataframe
    :param csv_files_list: list with file paths
    :return: DataFrame
    """
    try:
        return pd.read_csv(csv_files_path)
    except Exception as e:
        logger.error(f"csv parsing into dataframe failed with Ecxception {e} !")
        quit()


def main(xml_dir_path,csv_file_path) -> bool:
    '''
    This function is the starting point that calls other functions
            that does filter adn do other jobs
        Parameters:
            None

        Returns:
            value (bool): True or False
    '''
    logger.info("main function called!")
    xml_files_list = decompress_wiki_xml_file(xml_dir_path)
    extract_wiki_xml_into_pandas_df(xml_files_list)
    extract_metadata_csv_into_pandas_df(csv_file_path)
    logger.info("main function Ended Success!")


if __name__ == '__main__':
    main('./data','./data/raw_movies_metadata.csv.zip')
    