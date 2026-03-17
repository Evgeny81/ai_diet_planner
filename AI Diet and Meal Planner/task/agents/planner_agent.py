import json
from typing import List
from services.llm_client import LLMClient
from models import RecipeResponse, RecipeStep


class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, base_recipe: str) -> RecipeResponse:
        prompt = (
            f"You are a professional chef. Given the meal idea: \"{base_recipe}\"\n"
            "Create a detailed, complete cooking recipe.\n"
            "Return a JSON object with exactly these fields:\n"
            "  title: a descriptive recipe title (string),\n"
            "  ingredients: an array of ingredient strings,\n"
            "  steps: an array of objects, each with step_number (integer starting at 1) and instruction (string).\n"
            "Respond ONLY with valid JSON. No extra text."
        )
        result = self.llm.call_model_json(prompt)

        # Normalize steps if needed
        steps = []
        for i, step in enumerate(result.get("steps", [])):
            if isinstance(step, dict):
                step_number = step.get("step_number", i + 1)
                instruction = step.get("instruction", step.get("step", ""))
                steps.append(RecipeStep(step_number=step_number, instruction=instruction))
            elif isinstance(step, str):
                steps.append(RecipeStep(step_number=i + 1, instruction=step))

        # Normalize ingredients
        ingredients = []
        for ing in result.get("ingredients", []):
            if isinstance(ing, str):
                ingredients.append(ing)
            elif isinstance(ing, dict):
                ingredients.append(ing.get("name", ing.get("ingredient", str(ing))))

        return RecipeResponse(
            title=result.get("title", base_recipe),
            ingredients=ingredients,
            steps=steps,
        )

    def run_multiple(self, recipe_ideas: List[str], count: int = 5) -> List[RecipeResponse]:
        recipes = []
        for idea in recipe_ideas[:count]:
            recipe = self.run(idea)
            recipes.append(recipe)
        return recipes