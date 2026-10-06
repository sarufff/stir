import json
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

CACHE_PATH = "usda_cache.json"

with open("ml-experiments/recipes_cleaned.json", "r") as f:
    recipes = json.load(f)

try:
    with open(CACHE_PATH, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

unique_ingredients = set()
for recipe in recipes:
    for name in recipe["ingredients_clean"]:
        unique_ingredients.add(name)

remaining = [i for i in unique_ingredients if i not in cache]

print(f"Total unique ingredients: {len(unique_ingredients)}")
print(f"Already cached: {len(unique_ingredients) - len(remaining)}")
print(f"Remaining to look up: {len(remaining)}")


def lookup_food(name):
    params = {
        "api_key": API_KEY,
        "query": name,
        "dataType": "SR Legacy,Foundation",
        "pageSize": 1
    }

    try:
        resp = requests.get(SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    foods = data.get("foods", [])
    if not foods:
        return None

    top = foods[0]
    category = top.get("foodCategory")
    if isinstance(category, dict):
        category = category.get("description")

    return {
        "canonical_name": top.get("description"),
        "category": category
    }


for i, name in enumerate(remaining):
    cache[name] = lookup_food(name)
    time.sleep(0.4)

    if (i + 1) % 50 == 0:
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f)
        print(f"Progress: {i + 1}/{len(remaining)} — saved")

with open(CACHE_PATH, "w") as f:
    json.dump(cache, f)

print("Done.")