import os
import unittest
from website_specific_crawler import udnnews
import logging
import utilities
import config
import datetime


class TestUDNNews(unittest.TestCase):
    def setUp(self):
        self.keywords = utilities.retrieve_excel_keywords(os.path.join(config.DATA_DIRECTORY, r"關鍵字.xlsx"), "關鍵字活頁簿", "Category1")
        
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
    
    def test_crawl_keyword(self):
        keyword = "運動比賽"
        results = udnnews.crawl_keyword_date_range(keyword, start=datetime.date(2015, 1, 1), interval=1)
        utilities.dump_final_results(results, keyword, config.NewsProvider.UDN_NEWS.value)
        
    
    def test_crawl_keywords(self):
        for keyword in self.keywords:
            self.logger.info(f"Testing keyword: {keyword}")
            results = udnnews.crawl_keyword(keyword)
            utilities.dump_final_results(results, keyword, config.NewsProvider.UDN_NEWS.value)
        
if __name__ == '__main__':
    unittest.main()