# This is another sample python application that we may use to create the mealfinder
from flask import Flask, request, jsonify

app = Flask(__name)

# Mock recipe data
recipes = {
    "ingredient1": ["Recipe 1", "Recipe 2"],
    "ingredient2": ["Recipe 3", "Recipe 4"],
    # Add more data
}


@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    user_ingredients = request.json.get("ingredients")
    matching_recipes = []
    for ingredient in user_ingredients:
        if ingredient in recipes:
            matching_recipes.extend(recipes[ingredient])
    return jsonify({"recipes": matching_recipes})


if __name__ == "__main":
    app.run(debug=True)
