import os
import unittest
from src.news import newsFunctions_WebBased
from src.news import convert_to_excel


class TestExel(unittest.TestCase):
    def setUp(self):
        self.filename = r"output/filtered_results.xlsx"
        self.news_articles = newsFunctions_WebBased.retrieve_news_articles_from_file(r"output/progress.json")
    
    def test_classify_news_to_excel(self):
        convert_to_excel.classify_news_to_excel(self.news_articles, self.filename)