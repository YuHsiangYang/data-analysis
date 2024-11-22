import unittest
from src.llm import ChatGPT_BrowserBased as ChatGPT
import logging
from src.llm import token_utils


class TestChatGPT(unittest.TestCase):
    def setUp(self):
        self.prompt = "What is the meaning of life?"
        with open(
            r"C:\Users\yuhsi\SynologyDrive\Drive\成大\113 上\公共衛生學 (一)\筆記\transcript\2024-10-25 13-06-41 ---公共衛生學---.txt",
            "r",
            encoding="UTF-8",
        ) as file:
            self.transcript = file.read()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def test_GetChatGPTResponse(self):
        for i in range(10):
            response = ChatGPT.GetChatGPTResponse(self.prompt)
            self.logger.debug(f"Response: {response}")

    def test_tokenizer(self):
        token = token_utils.CalculateResponseCost(self.transcript, token_utils.Models.GPT_4O)
        logging.info(f"Token: {token}")
