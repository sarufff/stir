import json
from ingredient_parser import parse_ingredient

with open("recipes_parsed.json", "r") as f:
    recipes = json.load(f)

failed_count = 0


def clean_ingredient(raw):
    global failed_count
    try:
        parsed = parse_ingredient(raw)
    except Exception:
        failed_count += 1
        return None

    if not parsed.name:
        return None

    names = [n.text.lower().strip() for n in parsed.name]

    amount_text = None
    if parsed.amount:
        amount_text = parsed.amount[0].text

    return {
        "names": names,
        "amount": amount_text
    }


for recipe in recipes:
    cleaned = [clean_ingredient(i) for i in recipe["ingredients_raw"]]
    cleaned = [c for c in cleaned if c]
    recipe["ingredients_structured"] = cleaned
    recipe["ingredients_clean"] = [n for c in cleaned for n in c["names"]]

print(recipes[0]["ingredients_raw"])
print(recipes[0]["ingredients_structured"])
print(f"Failed to parse: {failed_count} ingredient lines")

with open("recipes_cleaned.json", "w") as f:
    json.dump(recipes, f)