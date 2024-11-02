import json
import time
import os
import config
import utilities
import pandas as pd


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
    #Check if the keyword files exist
    for keyword in keywords:
        file_name = f"{config.RESULTS_DIRECTORY}/{news_provider}/final_{news_provider}_{keyword}.json"
        if not os.path.exists(file_name):
            print(f"File {file_name} does not exist")
            Exception(f"Results file for keyword {keyword} does not exist")

        #Load the results file
        with open(file_name, 'r', encoding="UTF-8") as f:
            results = json.load(f)
            loaded_results.append({
                "keyword": keyword,
                "results": results
            })
    summary_sets = [set(result["summary"] for result in entry["results"]) for entry in loaded_results]
    common_summaries = set.intersection(*summary_sets)
    intersection_results = []
    for entry in loaded_results:
        for result in entry["results"]:
            if result["summary"] in common_summaries:
                intersection_results.append(result)
    return intersection_results
    dump_final_results(intersection_results, f"{" ".join(keywords)}", news_provider)
                    

    
    
def retrieve_excel_keywords(excel_file_path, sheet_name, column_name):
    # Read the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    # Access the named column
    column_data = df[column_name].dropna().tolist()

    return column_data

