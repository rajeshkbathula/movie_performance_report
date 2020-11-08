"""
unittest framework to test main script functions
"""

import unittest
import pandas as pd
from pandas.testing  import assert_frame_equal
from main import *
from schema_config import *

class TestmMainScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        thisdir = os.path.dirname(os.path.abspath(__file__))
        cls.raw_movies_metadata_csv_path = os.path.join(thisdir, './resources/raw_movies_metadata.csv.zip')
        cls.raw_wiki_abstract_xml_path = os.path.join(thisdir, './resources/raw_wiki_abstract.xml')
        wiki_csv_path = os.path.join(thisdir, './resources/wiki_df.csv')
        cls.wiki_df = pd.read_csv(wiki_csv_path,delimiter="§",engine='python')
        movies_metadata_csv_path = os.path.join(thisdir, './resources/movie_csv_df.csv')
        cls.movies_metadata_df = pd.read_csv(movies_metadata_csv_path, delimiter="§", engine='python')

    # def test_main_import(self):
    #     '''
    #     This function will test main script import work or no
    #     '''
    #     expected = True
    #     result = main()
    #     self.assertEqual(expected,result,"function from main import failing!")

    def test_extract_wiki_xml_into_pandas_df(self):
        '''
        This function will test xml parse into dataframe
        '''
        expected = extract_wiki_xml_into_pandas_df([self.raw_wiki_abstract_xml_path])
        self.assertEqual(expected['title'][0],self.wiki_df['title'][0],"wiki xml parse and into pandas df function failed!")
        self.assertNotEqual(expected['title'][0], self.wiki_df['title'][1],"wiki xml parse and into pandas df function failed!")

    def test_extract_metadata_csv_into_pandas_df(self):
        '''
        This function will test csv parse into dataframe
        '''
        expected = extract_metadata_csv_into_pandas_df(self.raw_movies_metadata_csv_path)
        assert_frame_equal(expected,self.movies_metadata_df,"metadata csv parse  into pandas df function failed!")


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
    