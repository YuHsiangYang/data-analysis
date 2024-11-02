import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
import LLM
import logging
import ChatGPTAPI

class Test_ChatGPT(unittest.TestCase):
    def setUp(self):
        # Configure the logger
        logging.basicConfig(
            level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        
    def test_filter_results(self):
        #Open the results file
        with open(r"final\聯合新聞網\final_聯合新聞網_霧霾.json", "r", encoding="UTF-8") as file:
            results = json.load(file)
            LLM.filterResults(results, "霧霾")
        

    def test_ask_question(self):
        # Test the chatGPT model
        question = "Hi"
        answer = LLM.chatGPT.askGPT(question)["response"]
        self.assertIsNotNone(answer)
        self.logger.info(answer)    
        
    @unittest.skip("Not in use")
    def test_websource_evaluation(self):
        # Get one topic at the time, and evaluate the quality of the source
        # The source should be a reliable source

        # Load the search results
        with open(r"testing files\output.json", "r", encoding="UTF-8") as file:
            search_results = json.load(file)
            
        self.assertIsNotNone(search_results)
        self.filtered_results = LLM.filterResults(search_results, )
        
        
if __name__ == '__main__':
    unittest.main()
    