from src.news import news_models

class IdentifyRelevanceBatchError(Exception):
    """Raises when there is an error in IdentifyRelevanceBatch function.
    This is used to pass the current progress of the function to the caller, so that the caller can continue the function from where it left off.

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, finished_news_articles: list[news_models.NewsArticle], message: str, processing_news_article: news_models.NewsArticle):
        self.finished_news_articles = finished_news_articles
        self.message = message
        self.processing_news_article = processing_news_article
        super().__init__(f"Error at news article: {processing_news_article}")