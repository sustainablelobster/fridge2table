"""Application factory"""

import os

from flask import current_app, Flask, jsonify, request

from .db import DatabaseHandler


def _get_database_handler() -> DatabaseHandler:
    """Get handle to database"""
    return DatabaseHandler("fridge2table.db")


def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def home():
        """Display main page"""
        return current_app.send_static_file("fridge2table.html")

    @app.route("/add_ingredients", methods=["POST"])
    def add_ingredients():
        """Add ingredients to database"""
        ingredients = request.json
        db_handler = _get_database_handler()

        for ingredient in ingredients:
            db_handler.add_user_ingredient(ingredient)

        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/remove_ingredients", methods=["POST"])
    def remove_ingredients():
        """Remove ingredients from database"""
        ingredients = request.json
        db_handler = _get_database_handler()

        for ingredient in ingredients:
            db_handler.remove_user_ingredient(ingredient)

        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/get_ingredients")
    def get_ingredients():
        """Get ingredients from database"""
        db_handler = _get_database_handler()
        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/get_recipes")
    def get_recipes():
        """Get recipes from database"""
        db_handler = _get_database_handler()
        recipes = db_handler.get_matching_recipes()
        return jsonify([x.to_dict() for x in recipes])

    return app
