"""
unittest framework to test main script functions
"""

import unittest,os,sys
from main import *

class TestmMainScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info(f"Running test cases Started!")
        cls.thisdir = os.path.dirname(os.path.abspath(__file__))
        cls.raw_movies_metadata_csv_path = os.path.join(cls.thisdir, './resources/raw_movies_metadata.csv.zip')
        cls.raw_wiki_abstract_xml_path = os.path.join(cls.thisdir, './resources/raw_wiki_abstract.xml')
        wiki_csv_path = os.path.join(cls.thisdir, './resources/wiki_df.csv')
        cls.wiki_df = pd.read_csv(wiki_csv_path,delimiter="§",engine='python')
        movies_metadata_csv_path = os.path.join(cls.thisdir, './resources/movie_csv_df.csv')
        cls.movies_metadata_df = pd.read_csv(movies_metadata_csv_path, delimiter="§", engine='python')

    def test_filter_bad_records(self):
        '''
        This function will test filter csv bad recods function giving back out put can include more like if removing or no bad records
        '''
        result_file = filter_bad_records(self.raw_movies_metadata_csv_path)
        try:
            with open(result_file,'r') as file :
                line = file.readline()
            result = line
        except Exception as e:
            result = None
        self.assertNotEqual(None,result,"filter bad records failing  ")

    def test_calc_ratio_and_profit_movie_filter(self):
        '''
        This function will test year extraction from date
        '''
        budget_limit_above = 10
        df = filter_profit_movies(self.movies_metadata_df,budget_limit_above)
        for index, value in df['revenue'].items():
            self.assertGreater(value,0,"revenue filter greater than 0 failed!")
        for index, value in df['budget'].items():
            self.assertGreater(value,0,"budget filter greater than 0 failed!")
        df = calc_ratio_from_budget_and_revenue_filter_top_once(df,3)
        expected_ratio = 1.1927757142857143
        result= df['revenue'][0]/ df['budget'][0]
        self.assertEqual(expected_ratio, result,"ratio not matching!")

    def test_extract_year_from_release_date(self):
        '''
        This function will test year extraction from date
        '''
        expected = 1995
        result = extract_year_from_release_date(self.movies_metadata_df)
        self.assertEqual(expected, result['year'][0],"date extraction from year failed!")

    def test_extract_wiki_xml_into_pandas_df(self):
        '''
        This function will test xml parse into dataframe
        '''
        top = 2
        df = filter_profit_movies(self.movies_metadata_df,2)
        result = extract_wiki_xml_into_pandas_df(self.raw_wiki_abstract_xml_path,df,top)
        expected = os.path.join(self.thisdir, './resources/raw_wiki_abstract_work.xml')
        self.assertEqual(result,expected,"wiki xml parse extraction function failed!")

        with open(expected,'r') as file:
            line = file.read()
        result_line_in_file = line
        result_list = [result_line_in_file.split("\n")[1]]
        expected_line_in_file = ['Smoke,https://en.wikipedia.org/wiki/Ayn_Rand,"[\'| birth_place = St. Petersburg, Russian Empire\']"']
        self.assertEqual(expected_line_in_file, result_list,"wiki xml parse and into pandas df function failed!")

    
    def test_string_ascii_check(self):
        '''
        This function will test given string asci or no function
        '''
        string = 'test'
        result = string_ascii_check(string)
        self.assertEqual(string,result, "string_ascii_check function failed!")
        string = 'За спичками'
        result = string_ascii_check(string)
        self.assertNotEqual(string,result, "string_ascii_check function failed!")

    def test_extract_metadata_csv_into_pandas_df(self):
        '''
        This function will test csv parse into dataframe
        '''
        result_df  = extract_metadata_csv_into_pandas_df(self.raw_movies_metadata_csv_path)
        result = result_df.budget.iloc[0],result_df.budget.iloc[-1], result_df.shape[0]
        expected = (7000000, 0,25)
        self.assertEqual(expected,result, "metadata csv parse  into pandas df function failed!")

    @classmethod
    def tearDownClass(cls):
        logger.info(f"Done Testing!")


if __name__ == '__main__':
    unittest.main()
    