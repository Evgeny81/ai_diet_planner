from fastapi import FastAPI
from models import (
    InventoryInput, InventoryResponse,
    DietInput, DietResponse,
    AskInput, AskResponse,
    PlanInput, RecipeResponse,
    RecommendInput, RecommendResponse,
)
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent
from agents.manager_agent import ManagerAgent
from agents.planner_agent import PlannerAgent
from app.logging import get_logger

logger = get_logger("app")

app = FastAPI(title="AI Diet & Meal Planner")

inventory_agent = InventoryAgent()
diet_agent = DietAgent()
manager_agent = ManagerAgent()
planner_agent = PlannerAgent()


@app.get("/")
async def root():
    return {"message": "Success!"}


@app.post("/inventory", response_model=InventoryResponse)
async def inventory(data: InventoryInput):
    return inventory_agent.run(data.items)


@app.post("/diet", response_model=DietResponse)
async def diet(data: DietInput):
    return diet_agent.run(data.items, data.diet)


@app.post("/ask", response_model=AskResponse)
async def ask(data: AskInput):
    logger.info("Received /ask request: items=%s, diet=%s", data.items, data.diet)
    result = manager_agent.run(data.items, data.diet)
    logger.info("/ask response: suggestions=%s", result["suggestions"])
    return result

@app.post("/plan", response_model=RecipeResponse)
async def plan(data: PlanInput):
    logger.info("Received /plan request: base_recipe=%s", data.base_recipe)
    result = planner_agent.run(data.base_recipe)
    logger.info("/plan response: title=%s", result.title)
    return result


@app.post("/recommend", response_model=RecommendResponse)
async def recommend(data: RecommendInput):
    logger.info("Received /recommend request: items=%s, diet=%s, recipe_count=%s", data.items, data.diet, data.recipe_count)
    manager_result = manager_agent.run(data.items, data.diet)
    suggestions = manager_result["suggestions"]
    recipes = planner_agent.run_multiple(suggestions, count=data.recipe_count)
    logger.info("/recommend response: %d recipes returned", len(recipes))
    return RecommendResponse(recipes=recipes)