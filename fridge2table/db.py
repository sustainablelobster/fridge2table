"""Provides class for handling database operations"""
import sqlite3

from .utils import dedup_list
from .types import Recipe


class DatabaseHandler:
    """Provides an interface to the recipe/ingredients database"""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)
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
            "CREATE TEMP TABLE user_ingredients (name TEXT PRIMARY KEY);"
        )

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
                ",".join(recipe.ingredients),
            ),
        )
        self._connection.commit()

    def add_user_ingredient(self, ingredient: str) -> None:
        """Add a user ingredient to the database"""
        self._cursor.execute(
            "INSERT OR IGNORE INTO user_ingredients (name) values (?)",
            (ingredient,),
        )
        self._connection.commit()

    def get_matching_recipes(self) -> list[Recipe]:
        """Get recipes matching user's ingredients"""
        user_ingredients = self.get_user_ingredients()
        matching_recipes = []
        for user_ingredient in user_ingredients:
            matching_recipes += self.get_recipes_containing_ingredient(user_ingredient)
        return dedup_list(matching_recipes)

    def get_user_ingredients(self) -> list[str]:
        """Return user's ingredients"""
        selection_cursor = self._cursor.execute("SELECT name FROM user_ingredients")
        return [x[0] for x in selection_cursor.fetchall()]

    def get_recipes_containing_ingredient(self, ingredient: str) -> list[Recipe]:
        """Return a list of recipes that contain the given ingredient"""
        selection_cursor = self._cursor.execute(
            "SELECT (name, url, image_url, ingredients) FROM recipes WHERE ingredients LIKE ?",
            (f"%{ingredient}%",),
        )
        recipes = []
        for selection in selection_cursor.fetchall():
            recipes.append(
                Recipe(
                    selection[0], selection[1], selection[2], selection[3].split(",")
                )
            )
        return recipes
