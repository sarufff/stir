import json
import re
import random

with open("recipes_parsed.json", "r") as f:
    recipes = json.load(f)

   # Common units/measurement words to strip out
UNITS = [
    "c\\.?", "cup", "cups", "tsp\\.?", "teaspoon", "teaspoons",
    "tbsp\\.?", "tablespoon", "tablespoons", "oz\\.?", "ounce", "ounces",
    "lb\\.?", "pound", "pounds", "pkg\\.?", "package", "packages",
    "can", "cans", "jar", "jars", "clove", "cloves", "pinch", "dash",
    "small", "medium", "large", "whole", "bite size", "shredded"
]
UNIT_PATTERN = r'\b(' + '|'.join(UNITS) + r')\b'

def clean_ingredient(raw):
    text = raw.lower()
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\d+\s*\/\s*\d+|\d+', '', text)
    text = re.sub(UNIT_PATTERN, '', text)
    text = re.sub(r'\b(firmly packed|finely chopped|chopped|sliced|diced|minced|fresh|softened|melted|to taste|or margarine)\b', '', text)
    text = re.sub(r'[.,;:]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

for recipe in recipes:
    recipe["ingredients_clean"] = [clean_ingredient(i) for i in recipe["ingredients_raw"]]
    recipe["ingredients_clean"] = [i for i in recipe["ingredients_clean"] if i]  # drop empties



sample_indices = random.sample(range(len(recipes)), 5)

for i in sample_indices:

    print(recipes[i]["ingredients_raw"])
    print(recipes[i]["ingredients_clean"])
    print("---")

with open("recipes_cleaned.json", "w") as f:
    json.dump(recipes, f)