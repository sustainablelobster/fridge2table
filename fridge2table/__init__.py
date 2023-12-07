"""Application factory"""

import os

from flask import Flask, current_app, jsonify, request

from .db import DatabaseHandler


def create_app():
    """Create and configure the app"""
    DatabaseHandler()  # ensure database is initialized before app starts
    app = Flask(__name__)

    @app.route("/")
    def home():
        """Display main page"""
        return current_app.send_static_file("index.html")

    @app.route("/favicon.ico")
    def favicon():
        """Return favicon"""
        return current_app.send_static_file("favicon.ico")

    @app.route("/add_ingredients", methods=["POST"])
    def add_ingredients():
        """Add ingredients to database"""
        ingredients = request.json
        db_handler = DatabaseHandler()

        for ingredient in ingredients:
            db_handler.add_user_ingredient(ingredient)

        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/remove_ingredients", methods=["POST"])
    def remove_ingredients():
        """Remove ingredients from database"""
        ingredients = request.json
        db_handler = DatabaseHandler()

        for ingredient in ingredients:
            db_handler.remove_user_ingredient(ingredient)

        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/get_ingredients")
    def get_ingredients():
        """Get ingredients from database"""
        db_handler = DatabaseHandler()
        ingredients = db_handler.get_user_ingredients()
        return jsonify(ingredients)

    @app.route("/get_recipes")
    def get_recipes():
        """Get recipes from database"""
        db_handler = DatabaseHandler()
        do_search = request.args.get("search", type=bool, default=False)
        recipes = db_handler.get_matching_recipes(do_search)
        return jsonify([x.to_dict() for x in recipes])

    @app.route("/searched_before")
    def searched_before():
        """Determine if current inventory of ingredients has been searched before"""
        db_handler = DatabaseHandler()
        return jsonify(db_handler.searched_before())

    return app
