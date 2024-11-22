from duckduckgo_search import DDGS
import json
import jsonschema
from jsonschema import validate
import time


def search(query_input, max_results=10):
    results = DDGS().text(query_input, max_results=max_results)
    return results


def search_by_json(query_input: json, max_results=10) -> json:
    # Get the subtopics from the json file
    subtopics = query_input["subtopics"]

    # Results
    search_results = []

    # Search for each subtopic
    for subtopic_obj in subtopics:
        result_per_subtopic = {
            "subtopic": subtopic_obj["subtopic"],
            "queries": {
                "query": subtopic_obj["searchQueries"],
                "results": []
            }
        }
        # iterate through each query in the subtopic
        # This is based on the queries_scheme.json file
        for query in subtopic_obj["searchQueries"]:
            # Search for the query
            query_result = DDGS().text(query, max_results=max_results)
            result_per_subtopic["queries"]["results"].append(query_result)
            
            # Add a delay for each run to avoid being blocked by the server
            time.sleep(3)

        search_results.append(result_per_subtopic)

    with open(r"JSON Schema\duckduckgo_ResultsFormat.json", 'r', encoding="UTF-8") as schema_file:
        schema = json.load(schema_file)

    # Validate the JSON data against the schema
    try:
        validate(instance=search_results, schema=schema)
        print("JSON data is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print("JSON data is invalid.")
        print(err)

    return search_results
