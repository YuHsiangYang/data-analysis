import tiktoken
import json
from enum import Enum

from dataclasses import dataclass


@dataclass
class APICost:
    input: float
    output: float


@dataclass
class ModelCost:
    model: str
    nonBatchAPI: APICost
    batchAPI: APICost

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            model=data["model"],
            nonBatchAPI=APICost(**data["nonBatchAPI"]),
            batchAPI=APICost(**data["batchAPI"])
        )

    def to_dict(self):
        return {
            "model": self.model,
            "nonBatchAPI": self.nonBatchAPI.__dict__,
            "batchAPI": self.batchAPI.__dict__
        }


class Models(Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_2024_11_20 = "gpt-4o-2024-11-20"
    GPT_4O_2024_08_06 = "gpt-4o-2024-08-06"
    GPT_4O_AUDIO_PREVIEW = "gpt-4o-audio-preview"
    GPT_4O_AUDIO_PREVIEW_2024_10_01 = "gpt-4o-audio-preview-2024-10-01"
    GPT_4O_2024_05_13 = "gpt-4o-2024-05-13"


def find_price_by_model(model_name) -> json:
    with open('src\llm\price_list.json', 'r', encoding='UTF-8') as file:
        price_list = json.load(file)
    for model in price_list:
        if model['model'] == model_name:
            return model
    return None


def CalculateResponseCost(input, model: Models) -> ModelCost:
    """
    Calculate the response cost of a given input based on the price per 1k characters.
    """

    encoder = tiktoken.encoding_for_model(model.value)

    token = encoder.encode(input)

    length = len(token)

    model_info = find_price_by_model(model.value)

    cost = ModelCost(
        model=model.value,
        nonBatchAPI=APICost(
            input=length *
            model_info["non_batchAPI"]["input_price_per_1M"] / 10000000,
            output=length *
            model_info["non_batchAPI"]["output_price_per_1M"] / 1000000
        ),
        batchAPI=APICost(
            input=length *
            model_info["batchAPI"]["input_price_per_1M"] / 1000000,
            output=length *
            model_info["batchAPI"]["output_price_per_1M"] / 1000000
        )
    )

    return cost
