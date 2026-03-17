import json
from typing import List
from services.llm_client import LLMClient
from models import DietResponse


class DietAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: List[str], diet: str) -> DietResponse:
        items_json = json.dumps(items)
        prompt = (
            f"You are a diet-aware kitchen assistant. Given the JSON array of ingredients:\n"
            f"{items_json}\n"
            f"and the dietary preference: {diet}\n"
            "Return a JSON object with:\n"
            "  compatible_items: an array of ingredients from the list that are compatible with the given diet (remove any that violate the diet),\n"
            "  suggested_recipe_ideas: an array of exactly 5 recipe ideas that use only the compatible ingredients and follow the dietary preference.\n"
            "Respond ONLY with valid JSON."
        )
        result = self.llm.call_model_json(prompt)
        return DietResponse(**result)