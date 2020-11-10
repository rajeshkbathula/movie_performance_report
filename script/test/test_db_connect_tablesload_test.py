"""
unittest framework to test Postgres connection and data load
"""
import unittest,os
import uuid
from main import *

class TestmMainScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.thisdir = os.path.dirname(os.path.abspath(__file__))
        movies_metadata_csv_path = os.path.join(cls.thisdir, './resources/movie_csv_df.csv')
        cls.movies_metadata_df = pd.read_csv(movies_metadata_csv_path, delimiter="§", engine='python')

    def test_postgres_connect(self):
        '''
        This function will test Postgres DB Connection
        '''
        try:
            connect = postgres_connect('test_user', 'psswd', 'test_db')
            result = connect.engine
            connect.close()
        except Exception as e:
            result = None
        expected = 'Engine(postgresql+psycopg2://test_user:***@localhost/test_db)'
        self.assertEqual(expected, str(result), "Pastgres DB function failed!")

    def test_postgres_feed(self):
        '''
        This function will test df load to pandas dataframe can be extended reading and texting data.
        '''
        test_table = f"test_{uuid.uuid1()}"
        connection = postgres_connect('test_user', 'psswd', 'test_db')
        inject_data = pandas_to_postgres_table(test_table,self.movies_metadata_df,connection)
        self.assertTrue(inject_data,"Pd to Postgres inject failed!")


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
