import json
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

CACHE_PATH = "usda_cache.json"

try:
    with open(CACHE_PATH, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}


def lookup_food(name):
    if name in cache:
        return cache[name]

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
    except Exception as e:
        cache[name] = None
        return None

    foods = data.get("foods", [])
    if not foods:
        cache[name] = None
        return None

    top = foods[0]
    category = top.get("foodCategory")
    if isinstance(category, dict):
        category = category.get("description")

    result = {
        "canonical_name": top.get("description"),
        "category": category
    }
    cache[name] = result
    return result


def save_cache():
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)


if __name__ == "__main__":
    test_items = ["chicken", "cream of chicken soup", "chicken breasts", "onion soup mix"]

    for item in test_items:
        result = lookup_food(item)
        print(f"{item}  ->  {result}")
        time.sleep(0.2)

    save_cache()