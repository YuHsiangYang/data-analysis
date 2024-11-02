import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
import utilities
import logging
import config


class Test_Utilities(unittest.TestCase):
    def setUp(self):
        # Configure the logger
        logging.basicConfig(
            level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
    def test_boolean_operation_on_results(self):
        for set_1 in utilities.retrieve_excel_keywords(os.path.join(config.DATA_DIRECTORY, "關鍵字.xlsx"), "聯集", "關鍵字1"):
            for set_2 in utilities.retrieve_excel_keywords(os.path.join(config.DATA_DIRECTORY, "關鍵字.xlsx"), "聯集", "關鍵字2"):
                keywords = [set_1, set_2]
                operation = "and"
                news_provider = config.NewsProvider.UDN_NEWS.value
                results = utilities.boolean_operation_on_results(keywords, operation, news_provider)
                utilities.dump_final_results(results, keywords, news_provider, os.path.join(config.UNION_RESULTS_DIRECTORY, f"final_{news_provider}_{' '.join(keywords)}.json"))                
        
        
if __name__ == '__main__':
    unittest.main()
    