"""
unittest framework to test main script functions
"""

import unittest
import pandas_read_xml as pdx
import pandas as pd
from main import *

class TestmMainScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        thisdir = os.path.dirname(os.path.abspath(__file__))
        raw_movies_metadata_csv_path = os.path.join(thisdir, './resources/raw_movies_metadata.csv')
        cls.raw_movies_metadata_csv_df = pd.read_csv(raw_movies_metadata_csv_path)
        raw_wiki_abstract_xml_path = os.path.join(thisdir, './resources/raw_wiki_abstract.xml')
        cls.raw_wiki_abstract_df = pdx.read_xml(raw_wiki_abstract_xml_path, ['feed', 'doc'])

    def test_main_import(self):
        '''
        This function will test main script import work or no
        '''
        expected = True
        result = main()
        self.assertEqual(expected,result,"function from main import failing!")


    @classmethod
    def tearDownClass(cls):
        cls.raw_movies_metadata_csv_df.dropna()
        cls.raw_wiki_abstract_df.dropna()

if __name__ == '__main__':
    unittest.main()
    