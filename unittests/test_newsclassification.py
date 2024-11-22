import utilities
import LLM
import config
import unittest
import logging
import json
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class test_GeneratePerformance(unittest.TestCase):
    def setUp(self):
        self.theme_description = "主要是需要了解馬拉松和空汙的關係，以及空汙對馬拉松的影響，如果文章沒有提到這些或是跟這些無關，就不要放進來"
        self.theme = "馬拉松跟空汙的關係"
        self.news_provider = config.NewsProvider.UDN_NEWS.value

        # Configure the logger
        logging.basicConfig(
            level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

        # If the LLM identifies correctly, then variables below should be true.
        self.results_related = []
        self.results_unrelated = []
        self.results_mixed = []
        self.mixed_results_answers = []
    
    def test_read_news_from_directory(self):
        news_articles = utilities.read_news_articles_from_directory(config.UNION_RESULTS_DIRECTORY)
        self.logger.debug(f"News articles: {news_articles}")

    def test_filter(self):
        #Import the news articles using read_news_from_directory
        raw_news_articles = utilities.read_news_articles_from_directory(os.path.join(config.UNION_RESULTS_DIRECTORY))
        #Import both related and unrelated articles from the directory as processed by LLM
        processed_articles = utilities.read_news_articles_from_directory(config.FILTERED_DIRECTORY)
        
        
        #Filter the news article by news provider
        raw_news_articles = [news_article for news_article in raw_news_articles if news_article["news_provider"] == self.news_provider]
        
        processed_hrefs = [news_article["href"] for news_article in processed_articles]
        
        self.logger.debug(f"Processed articles: {processed_articles}")
        
        for news_article in raw_news_articles:
            #Check if the news article is already processed
            if news_article["href"] in processed_hrefs:
                continue
            
            is_related = LLM.identify_relevance(news_article, self.theme, self.theme_description)
            if is_related:
                self.results_related.append(news_article)
            else:
                self.results_unrelated.append(news_article)
            
            
            #Writ the related news article to the directory
            #Read the related articles from the file
            utilities.append_to_json_file(os.path.join(config.FILTERED_DIRECTORY, news_article["news_provider"], f"{news_article["filename"]}_filtered.json"), self.results_related)
                
                
            #Writ the unrelated news article to the directory
            utilities.append_to_json_file(os.path.join(config.FILTERED_DIRECTORY, news_article["news_provider"], "unrelated_articles.json"), self.results_unrelated)
                                    
    def test_generate_mixed_results(self):
        """
        Generate mixed results for testing
        """
        
        # import both related and unrelated articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "related.json"), "r", encoding="UTF-8") as file:
            related_articles = json.load(file)
            for article in related_articles:
                article['is_related'] = True

        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            unrelated_articles = json.load(file)
            for article in unrelated_articles:
                article['is_related'] = False
                
        # combine the articles
        mixed_articles = related_articles + unrelated_articles

        # shuffle the articles
        import random
        random.shuffle(mixed_articles)

        # store the answers to a variable
        self.mixed_results_answers = mixed_articles

        # store the answers to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed_answers.json"), "w", encoding="UTF-8") as file:
            json.dump(self.mixed_results_answers, file, ensure_ascii=False)

        mixed_results = []
        # generate the mixed results
        for article in mixed_articles:
            news_article = {
                "title": article["title"],
                "href": article["href"],
                "summary": article["summary"],
                "publication_date": article["publication_date"]
            }

            mixed_results.append(news_article)

        # write the mixed results to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed.json"), "w", encoding="UTF-8") as file:
            json.dump(mixed_results, file, ensure_ascii=False)

    def test_related_articles(self):
        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "related.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_related.append(is_related)
                # break

        self.logger.debug(f"Related results: {self.results_related}")

    def test_unrelated_articles(self):

        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_unrelated.append(is_related)

        self.logger.debug(f"Unrelated results: {self.results_unrelated}")

    def test_mixed_articles(self):
        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_mixed.append(is_related)
                # # check with the answers
                # # Import the answers
                # with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed_answers.json"), "r", encoding="UTF-8") as file:
                #     answers = json.load(file)
                #     for answer in answers:
                #         if answer['title'] == news_article['title']:
                #             self.results_mixed.append(
                #                 answer['is_related'] == is_related)
        self.logger.debug(f"Mixed results: {self.results_mixed}")

    def test_generate_performance(self):
        # Generate the performance
        performance = {
            "related": sum(self.results_related),
            "unrelated": sum(self.results_unrelated),
            "mixed": self.results_mixed
        }

        # write the performance to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "performance.json"), "w", encoding="UTF-8") as file:
            json.dump(performance, file, ensure_ascii=False)


if __name__ == '__main__':
    unittest.main()
