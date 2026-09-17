from datasets import load_dataset
import json
import re

dataset = load_dataset("corbt/all-recipes", split="train")

   # We'll only use a manageable slice to start — 50,000 recipes
subset = dataset.select(range(50000))

parsed_recipes = []

for row in subset:
    text = row["input"]
       
       # Split into title / ingredients / directions using the known format
    try:
        title_part, rest = text.split("\n\n", 1)
        ingredients_part, directions_part = rest.split("Directions:", 1)
        ingredients_raw = ingredients_part.replace("Ingredients:", "").strip()
           
           # Extract just ingredient lines
        ingredient_lines = [line.strip("- ").strip() for line in ingredients_raw.split("\n") if line.strip()]
           
        parsed_recipes.append({
            "title": title_part.strip(),
            "ingredients_raw": ingredient_lines,
            "full_text": text
        })
    except ValueError:
        continue  # skip malformed entries

print(f"Parsed {len(parsed_recipes)} recipes successfully")
print(parsed_recipes[0])

with open("recipes_parsed.json", "w") as f:
    json.dump(parsed_recipes, f)
