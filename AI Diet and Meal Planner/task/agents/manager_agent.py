from typing import List, Dict, Any
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent


class ManagerAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, items: List[str], diet: str) -> Dict[str, Any]:
        # Step 1: Clean and validate items via InventoryAgent
        inventory_result = self.inventory_agent.run(items)

        # Step 2: Filter by diet and get suggestions via DietAgent
        diet_result = self.diet_agent.run(inventory_result.usable_items, diet)

        # Step 3: Return combined structured response
        return {
            "usable_items": inventory_result.usable_items,
            "diet_filtered": diet_result.compatible_items,
            "suggestions": diet_result.suggested_recipe_ideas,
        }