import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website_specific_crawler import nextapple
import unittest
import utilities

class Test_nextapple(unittest.TestCase):
    def setUp(self):
        self.keyword = "PM2.5"
        self.keywords = utilities.retrieve_excel_keywords("關鍵字.xlsx", "關鍵字活頁簿", "Category2")
        
    
    def test_crawl_keyword_excel(self):
        for keyword in self.keywords:
            if not os.path.exists(f"final/final_蘋果日報_{keyword}.json"):
                output = nextapple.crawl_keyword(keyword)
                utilities.dump_final_results(output, keyword, "蘋果日報")
    @unittest.skip("Taking a break now")         
    def test_crawl_keyword(self):
        output = nextapple.crawl_keyword(self.keyword)
        utilities.dump_final_results(output, self.keyword)
    
    @unittest.skip("Taking a break now")
    def test_boolean_operation_on_results(self):
        output = utilities.boolean_operation_on_results(self.keywords, "and")
        print(output)
        
        
        
if __name__ == '__main__':
    unittest.main()