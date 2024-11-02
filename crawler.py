from duckduckgo_search import DDGS
import json


def searchQuery(query: str, number_of_results: int = 10) -> json:
    """This function utilizes duckduckgo to search for the query and returns the results

    Args:
        query (str): the specific query to search for
        number_of_results (int, optional): number of results to use. Defaults to 10.

    Returns:
        list: a list of the results with title, short summary, and link
    """
    
    results = DDGS().text(query, max_results=number_of_results)
    json_str = json.dumps(results)
    parsed_results = json.loads(json_str)
    
    return parsed_results


def getWebsiteContents(url: str) -> json:
    """Access the web and get the contents of the web page

    Args:
        url (str): url of the web page

    Returns:
        json: with title, contents, and link to the article
    """