import unittest
from src.out_table import table_printout
from src.parse_args import parse_args
import sys, os, tempfile
from pathlib import Path
import pandas as pd

def _get_expect_dir():
    cur_dir = os.path.dirname(__file__)
    expect_dir = os.path.join(cur_dir, 'fixtures')
    return expect_dir

class TestOutPrint(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()
    
    def test_out_table1(self):
        
        df_1 = pd.read_csv('tests/base_files/out_table_1.csv')
        
        tb_1 = '+-------+----------------+----------------+-------+\n| time  |      day1      |      day2      | day3  |\n+-------+----------------+----------------+-------+\n| 9:00  | loc1-item1-p1  |                |       |\n|       | loc2-item1-p2  |                |       |\n| 9:30  |                | loc4-item3-p3  |       |\n+-------+----------------+----------------+-------+\n'
        
        self.assertEqual(table_printout(df_1), tb_1)

    def test_out_table2(self):
        tb_2 = '+-------+----------------+----------------+-------+\n| time  |      day1      |      day2      | day3  |\n+-------+----------------+----------------+-------+\n| 9:00  |                | loc1-item1-p1  |       |\n|       | loc2-item1-p2  |                |       |\n| 9:30  |                | loc4-item3-p3  |       |\n+-------+----------------+----------------+-------+\n'

        df_2 = pd.read_csv('tests/base_files/out_table_2.csv')
        self.assertEqual(table_printout(df_2), tb_2)

if __name__ == '__main__':
    unittest.main()