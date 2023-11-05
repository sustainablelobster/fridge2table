"""Provides class for handling database operations"""
import sqlite3

from .types import Recipe


class DatabaseHandler:
    """Provides an interface to the recipe/ingredients database"""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)
        self._cursor = self._connection.cursor()

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS recipes ("
            + "id INTEGER PRIMARY KEY,"
            + "name TEXT NOT NULL,"
            + "url TEXT NOT NULL,"
            + "image_url TEXT,"
            + "UNIQUE (name, url, image_url)"
            + ");"
        )

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS ingredients ("
            + "id INTEGER PRIMARY KEY,"
            + "name TEXT NOT NULL,"
            + "UNIQUE (name)"
            + ");"
        )

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS recipe_ingredients ("
            + "recipe_id INTEGER,"
            + "ingredient_id INTEGER,"
            + "FOREIGN KEY (recipe_id) REFERENCES recipes (id) "
            + "ON UPDATE CASCADE ON DELETE CASCADE,"
            + "FOREIGN KEY (ingredient_id) REFERENCES ingredients (id) "
            + "ON UPDATE CASCADE ON DELETE CASCADE,"
            + "PRIMARY KEY (recipe_id, ingredient_id),"
            + "UNIQUE (recipe_id, ingredient_id)"
            + ");"
        )

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_ingredients ("
            + "name TEXT PRIMARY KEY"
            + ");"
        )

        self._connection.commit()

    def __del__(self):
        self._connection.commit()
        self._connection.close()

    def add_recipe(self, recipe: Recipe) -> None:
        """Add a recipe to the database"""
        self._cursor.execute(
            "INSERT OR IGNORE INTO recipes (name, url, image_url) VALUES (?, ?, ?);",
            (recipe.name, recipe.url, recipe.image_url),
        )

        for ingredient in recipe.ingredients:
            self._cursor.execute(
                "INSERT OR IGNORE INTO ingredients (name) VALUES (?);", (ingredient,)
            )

            self._cursor.execute(
                "INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id) "
                + "VALUES ("
                + "(SELECT id FROM recipes WHERE name = ?),"
                + "(SELECT id FROM ingredients WHERE name = ?)"
                + ");",
                (recipe.name, ingredient),
            )

        self._connection.commit()

    def add_user_ingredient(self, ingredient: str) -> None:
        """Add a user ingredient to the database"""
        self._cursor.execute(
            "INSERT OR IGNORE INTO user_ingredients (name) values (?)", (ingredient,)
        )
        self._connection.commit()
