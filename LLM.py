import json
import ChatGPTAPI as chatGPT
import re


def formulateQueries(searchPrompt) -> json:
    """Uses the LLM to formulate queries based on the search prompt

    Args:
        searchPrompt (string): the prompt from the user

    Raises:
        Exception: When chatgpt does not follow the instructions properly

    Returns:
        json: a json object containing the queries and the topics and subtopics
    """

    # This reads the flie that contains the instructions for formulating queries
    with open(r"instructions\formulate_queries.md", "r", encoding="UTF-8") as file:
        formulate_queries_Instruction = file.read()

        # Replace _prompt_ with the search prompt
        formulate_queries_Instruction = formulate_queries_Instruction.replace(
            "_prompt_", searchPrompt)

        # Uses google chrome to get the response from ChatGPT
        response_str = chatGPT.askGPT(formulate_queries_Instruction)["response"]

        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = json_pattern.search(response_str)

        if match:
            response_str = match.group(1)
        else:
            raise Exception(
                "No JSON code found in the response, ChatGPT may not follow the instructions properly" + "\n" + "prompt:" + searchPrompt)

        # Convert the response_str from string to json object
        response_json = json.loads(response_str)
        return response_json


def identify_relevance(news_article: json, theme: str, theme_description: str) -> list:
    # Import the intructions for identifying relevance
    with open(r"instructions\filter_news_one_by_one.md", "r", encoding="UTF-8") as file:
        filter_news_results_Instruction = file.read()

        # Remove link from the news article
        article_without_link = {
            "title": news_article["title"],
            "summary": news_article["summary"]
        }

        # Convert results to string
        results_str = json.dumps(article_without_link, ensure_ascii=False)

        response = chatGPT.customInstructions(filter_news_results_Instruction,
                                              {
                                                  "__news_article_summary__": results_str,
                                                  "__theme__": theme,
                                                  "__theme_description__": theme_description
                                              })["response"]

        # Check if the response is a list
        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = json_pattern.search(response)

        if match:
            response = match.group(1)
        else:
            raise Exception(
                "No JSON code found in the response, ChatGPT may not follow the instructions properly" + response)

        response_json = json.loads(response)
        is_related = response_json["is_related"]

    return is_related


def filterResults(results: json, search_prompt: str) -> json:
    """Uses LLM to filter the relevant results from the search results

    Args:
        results (json): search results from duckduckgo in the format defined by duckduckgo_direct_results.json

    Returns:
        json: an array with the relevant results
    """
    results_per_batch = 10

    # This reads the flie that contains the instructions for filtering results
    with open(r"instructions\filter_results.md", "r", encoding="UTF-8") as file:
        filter_results_Instruction = file.read()

        # Replace _topic_ with the search_prompt
        filter_results_Instruction = filter_results_Instruction.replace(
            "_topic_", search_prompt)

        # Process the results batch by batch
        for i in range(0, len(results), results_per_batch):
            # Get the batch of results
            results_batch = results[i:i+results_per_batch]

            # Convert the batch of results to string
            results_str = json.dumps(results_batch, ensure_ascii=False)

            # Replace _searchresults_ with results
            filter_results_Instruction = filter_results_Instruction.replace(
                "_searchresults_", results_str)

            # Use ChatGPT to get the response
            response_str = chatGPT.askGPT(filter_results_Instruction)["response"]
            print(response_str)
