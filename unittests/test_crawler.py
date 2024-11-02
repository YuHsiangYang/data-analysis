import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import LLM
import logging
import json
import duckduckgo
import config
import ChatGPTAPI

# Test the LLM class
class Test_LLM(unittest.TestCase):
    def setUp(self):
        #Set up code here
        self.prompt = "馬拉松跟空汙是甚麼關係?"
        
        #Configure the logger
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.search_queries = []
    def test_formulateQueries(self):
        self.search_queries = LLM.formulateQueries(self.prompt)
        
        #Check if the results are not None
        self.assertIsNotNone(self.search_queries)
        
        #Log the results 
        self.logger.info(f"Test formulateQueries with prompt '{self.prompt}'")
        self.logger.info(f"Results: {self.search_queries}")

        # # Ensure search_queries is a dictionary with a "subtopics" key
        # self.assertIsInstance(self.search_queries, dict)
        self.assertIn("subtopics", self.search_queries)
        
        #This part uses the results from formulateQueries to begin a search using the json format
        self.results = duckduckgo.search_by_json(self.search_queries, max_results=10)
        self.logger.info("Testing the combination of formulate queries and search using the formulated json file")
        self.logger.info(f"Prompt: {self.results}")
        
        with open(r"testing files\output.json", "w", encoding="UTF-8") as file:
            file.write(json.dumps(self.results, ensure_ascii=False))
        
class test_FilterResults(unittest.TestCase):
    def setUp(self):
        self.results_dir = config.UNION_RESULTS_DIRECTORY
        self.theme_description = "主要是需要了解馬拉松和空汙的關係，以及空汙對馬拉松的影響，如果文章沒有提到這些或是跟這些無關，就不要放進來"
        self.theme = "馬拉松跟空汙的關係"
        # Configure the logger
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
    
    def test_filterResults(self):
        # Open the results file in the directory
        files = os.listdir(self.results_dir)

        # for results_file in files:
        with open(r"聯集\final_蘋果日報_AQI 運動.json", "r", encoding="UTF-8") as file:
            results = json.load(file)
            relevant_results = []
            for result in results:
                related = LLM.identify_relevance(result, self.theme, self.theme_description)
                if related:
                    relevant_results.append(result)
                self.logger.debug(f"Identified: {related}")
                break
            self.logger.debug(f"Results: {relevant_results}")
            
        

if __name__ == '__main__':
    unittest.main()