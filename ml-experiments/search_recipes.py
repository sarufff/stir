import json

with open("recipes_cleaned.json", "r") as f:
    recipes = json.load(f)

def normalize(text):
    return text.lower().strip()

def ingredient_matches(pantry_item, recipe_ingredient):
    pantry_item = normalize(pantry_item)
recipe_ingredient = normalize(recipe_ingredient)
    return pantry_item in recipe_ingredient or recipe_ingredient in pantry_item

def score_recipe(pantry_items, recipe):
    recipe_ingredients = recipe["ingredients_clean"]
matched = []
missing = []

for ing in recipe_ingredients:
    found = any(ingredient_matches(p, ing) for p in pantry_items)
    if found:
        matched.append(ing)
    else:
        missing.append(ing)

total = len(recipe_ingredients)
match_ratio = len(matched) / total if total > 0 else 0

return {
    "title": recipe["title"],
    "full_text": recipe["full_text"],
    "matched": matched,
    "missing": missing,
    "match_ratio": match_ratio
}

def find_recipes(pantry_items, min_ratio=0.6, limit=10):
scored = [score_recipe(pantry_items, r) for r in recipes]
good_matches = [s for s in scored if s["match_ratio"] >= min_ratio]
good_matches.sort(key=lambda x: x["match_ratio"], reverse=True)
return good_matches[:limit]

if __name__ == "__main__":
test_pantry = ["chicken", "onion", "cheese", "flour tortillas", "sour cream"]
results = find_recipes(test_pantry)

print(f"Found {len(results)} matching recipes")
for r in results:
    print(f"\n{r['title']} — {r['match_ratio']:.0%} match")
    print(f"Have: {r['matched']}")
    print(f"Missing: {r['missing']}")

