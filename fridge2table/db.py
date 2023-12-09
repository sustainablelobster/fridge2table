"""Provides class for handling database operations"""
import importlib
import json
import os
import sqlite3

from .utils import dedup_list
from .types import Recipe


class DatabaseHandler:
    """Provides an interface to the recipe/ingredients database"""

    _DB_PATH = os.path.join(os.path.expanduser("~"), ".fridge2table.db")
    _LIST_DELIMITER = "|"

    def __init__(self):
        self._connection = sqlite3.connect(self._DB_PATH)
        self._cursor = self._connection.cursor()

        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                image_url TEXT,
                ingredients TEXT,
                UNIQUE (name, url, image_url, ingredients)
            );
            """
        )

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_ingredients (name TEXT PRIMARY KEY);"
        )

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS searches (ingredients TEXT PRIMARY KEY);"
        )

        if not self._has_recipes():
            self._add_cached_recipes()

        self._connection.commit()

    def __del__(self):
        self._connection.commit()
        self._connection.close()

    def add_recipe(self, recipe: Recipe) -> None:
        """Add a recipe to the database"""
        self._cursor.execute(
            """
            INSERT OR IGNORE INTO recipes (name, url, image_url, ingredients)
                VALUES (?, ?, ?, ?);
            """,
            (
                recipe.name,
                recipe.url,
                recipe.image_url,
                self._stringify_list(recipe.ingredients),
            ),
        )
        self._connection.commit()

    def add_user_ingredient(self, ingredient: str) -> None:
        """Add a user ingredient to the database"""
        self._cursor.execute(
            "INSERT OR IGNORE INTO user_ingredients (name) values (?);",
            (ingredient,),
        )
        self._connection.commit()

    def remove_user_ingredient(self, ingredient: str) -> None:
        """Remove a user ingredient from the database"""
        self._cursor.execute(
            "DELETE FROM user_ingredients WHERE name = ?;",
            (ingredient,),
        )
        self._connection.commit()

    def get_matching_recipes(self) -> list[Recipe]:
        """Get recipes matching user's ingredients, sorted from most to least relevant"""
        user_ingredients = self.get_user_ingredients()
        matching_recipes = []

        for user_ingredient in user_ingredients:
            matching_recipes += self.get_recipes_containing_ingredient(user_ingredient)

        matching_recipes = dedup_list(matching_recipes)
        matching_recipes.sort(key=lambda x: x.rank(user_ingredients), reverse=True)
        return matching_recipes

    def get_user_ingredients(self) -> list[str]:
        """Return user's ingredients"""
        selection = self._cursor.execute("SELECT name FROM user_ingredients;")
        return [x[0] for x in selection.fetchall()]

    def get_recipes_containing_ingredient(self, ingredient: str) -> list[Recipe]:
        """Return a list of recipes that contain the given ingredient"""
        selection = self._cursor.execute(
            "SELECT name,url,image_url,ingredients FROM recipes WHERE ingredients LIKE ?;",
            (f"%{ingredient}%",),
        )
        recipes = []
        for item in selection.fetchall():
            recipes.append(
                Recipe(
                    item[0],
                    item[1],
                    item[2],
                    self._destringify_list(item[3]),
                )
            )
        return recipes

    def searched_before(self) -> bool:
        """Determine if current inventory of ingredients has been searched before"""
        selection = self._cursor.execute(
            "SELECT * FROM searches WHERE ingredients = ?;",
            (self._stringify_list(self.get_user_ingredients()),),
        )
        return selection.fetchone() is not None

    def get_recipe_urls(self) -> list[str]:
        """Return list of all recipe urls in database"""
        selection = self._cursor.execute("SELECT url FROM recipes")
        return [x[0] for x in selection.fetchall()]

    def save_search(self) -> None:
        """Save the current inventory of ingredients to the search table"""
        self._cursor.execute(
            "INSERT OR IGNORE INTO searches (ingredients) values (?);",
            (self._stringify_list(self.get_user_ingredients()),),
        )
        self._connection.commit()

    def _has_recipes(self) -> bool:
        """Determine if database has no recipes"""
        selection = self._cursor.execute("SELECT * FROM recipes;")
        return selection.fetchone() is not None

    def _add_cached_recipes(self) -> None:
        with importlib.resources.open_text(
            "fridge2table.resources", "cached_recipes.json"
        ) as f:
            for recipe_dict in json.load(f):
                recipe = Recipe(**recipe_dict)
                self.add_recipe(recipe)
        self._connection.commit()

    @classmethod
    def _stringify_list(cls, l: list[str]) -> str:
        """Convert a list to a string for storing in database"""
        sorted_list = sorted(l)
        return cls._LIST_DELIMITER.join(sorted_list)

    @classmethod
    def _destringify_list(cls, list_string: str) -> list[str]:
        """Unpack a stringified list"""
        return list_string.split(cls._LIST_DELIMITER)
