import json
import time
import os
import config
import utilities
import pandas as pd


def dump_filtered_results(news_collection, theme_description, theme, news_provider, keyword_input: list, output_filepath_with_name):
    """Dump the results to a file

    Args:
        news_collection (json): a news object
        theme_description (str): theme description for the news
        theme (str): Short title for the theme
        news_provider (str): News provider of the filtered results
        keyword_input (list): a list of keywords used for the filtered results
    """

    dump_object = {
        "theme": theme,
        "theme_description": theme_description,
        "news_provider": news_provider,
        "keyword_input": keyword_input,
        "filtered_news": news_collection
    }

    with open(output_filepath_with_name, "w", encoding="UTF-8") as output_file:
        json.dump(dump_object, output_file, ensure_ascii=False, indent=4)


def dump_temp_results(news_collection, keyword_input, current_page_number, news_provider):
    """
    Dump the news_array to a temporary file
    """

    time_stamp = time.strftime("%Y%m%d%H%M%S")
    directory = "temp"
    file_name = f"temp_{news_provider}_{keyword_input}.json"
    object_to_dump = {
        "keyword": keyword_input,
        "current_page": current_page_number,
        "time_stamp": time_stamp,
        "news_array": news_collection
    }
    full_path = os.path.join(directory, file_name)
    with open(full_path, 'w', encoding="UTF-8") as f:
        json.dump(object_to_dump, f, ensure_ascii=False, indent=4)


def dump_final_results(news_collection, keyword_input, news_provider, path=""):
    """
    Dump the news_array to a final file
    """

    directory = config.RESULTS_DIRECTORY
    file_name = f"final_{news_provider}_{keyword_input}.json"
    object_to_dump = news_collection
    full_path = os.path.join(directory, news_provider, file_name)

    if path:
        full_path = path

    with open(full_path, 'w', encoding="UTF-8") as f:
        json.dump(object_to_dump, f, ensure_ascii=False, indent=4)


def boolean_operation_on_results(keywords, operation="and", news_provider=""):

    loaded_results = []
    # Check if the keyword files exist
    for keyword in keywords:
        file_name = f"{
            config.RESULTS_DIRECTORY}/{news_provider}/final_{news_provider}_{keyword}.json"
        if not os.path.exists(file_name):
            print(f"File {file_name} does not exist")
            Exception(f"Results file for keyword {keyword} does not exist")

        # Load the results file
        with open(file_name, 'r', encoding="UTF-8") as f:
            results = json.load(f)
            loaded_results.append({
                "keyword": keyword,
                "results": results
            })
    summary_sets = [set(result["summary"] for result in entry["results"])
                    for entry in loaded_results]
    common_summaries = set.intersection(*summary_sets)
    intersection_results = []
    for entry in loaded_results:
        for result in entry["results"]:
            if result["summary"] in common_summaries:
                intersection_results.append(result)
    return intersection_results


def append_to_json_file(file_path, new_objects):
    # Step 1: Read the existing JSON file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="UTF-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Step 2: Append the new objects to the list
    if isinstance(data, list):
        data.extend(new_objects)
    else:
        raise ValueError("The JSON file does not contain an array")

    # Step 3: Write the updated list back to the JSON file
    with open(file_path, "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_news_articles_from_directory(directory):
    news_articles = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r", encoding="UTF-8") as file:
                    news_articles_in_a_file = json.load(file)
                    for news_article in news_articles_in_a_file:
                        try:
                            news_article["keywords"] = file_name.split(".")[0].split("_")[
                                2].split(" ")
                            news_article["news_provider"] = file_name.split(".")[
                                0].split("_")[1]
                        except IndexError:
                            pass
                        news_article["filename"] = file_name.split(".")[0]
                        news_articles.append(news_article)

    return news_articles


def retrieve_excel_keywords(excel_file_path, sheet_name, column_name):
    # Read the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    # Access the named column
    column_data = df[column_name].dropna().tolist()

    return column_data
