import unittest
from src.news import newsFunctions_WebBased
from src.news import news_models
import json
from src.news import newsFunctionExceptions
import logging


class TestNews(unittest.TestCase):
    def setUp(self):
        self.news_directory = r"C:\Users\yuhsi\repos\web crawler (private version)\資料\資料交集_新"
        self.theme = news_models.Theme("空汙對馬拉松的影響", "本主題著重探討馬拉松與空氣污染之間的關係，特別是分析空汙如何影響馬拉松賽事、參賽者及其表現。僅收錄直接涉及這些內容的文章或資料，與主題無關者請勿納入。")
        logging.basicConfig(
            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    def test_retrieve_news_articles_from_folder(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(self.news_directory)
        self.logger.debug(f"News articles: {news_articles}")
        self.logger.debug(f"Number of news articles: {len(news_articles)}")
    
    def test_IdentifyRelevance(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(self.news_directory)
        
        news_article = newsFunctions_WebBased.news_models.NewsArticle.from_dict(news_articles[0].to_dict())
        is_relevant = newsFunctions_WebBased.IdenfityRelevance(news_article, self.theme)
        
        self.logger.debug(f"Is relevant: {is_relevant}")
        
    def test_identifyRelevance_Loop(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(self.news_directory)
        self.logger.debug(f"Number of news articles: {len(news_articles)}")
        for news_article in news_articles:
            is_relevant = newsFunctions_WebBased.IdenfityRelevance(news_article, self.theme)
            self.logger.error(f"Is relevant: {is_relevant}")
    
    def test_IdentifyRelevanceBatch(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(self.news_directory)
        self.logger.debug(f"Number of news articles: {len(news_articles)}")
        try:
            self.logger.debug("type: " + str(type(news_articles[0])))
            relevance = newsFunctions_WebBased.IdentifyRelevanceBatch(news_articles, self.theme, progress_callback=newsFunctions_WebBased.log_progress)
            self.logger.debug(f"Relevance: {relevance}")
        except newsFunctionExceptions.IdentifyRelevanceBatchError as e:
            # Log the processed news articles as temp
            temp_file = "output/temp.json"
            articles_dict = [article.to_dict() for article in e.finished_news_articles]
            with open(temp_file, "w", encoding="UTF-8") as file:
                json.dump(articles_dict, file, ensure_ascii=False, indent=4)
            self.logger.error(e.message)
            