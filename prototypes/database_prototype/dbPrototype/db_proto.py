"""module providing necessary functions for sqlite3"""
import sqlite3
from sqlite3 import Error


class DbProto:
    """
    This python class is used for sqlite3 database operations
    this class contains preset functions and queries to:
    create tables
    update tables / records
    return queries
    """

    # The following are pre made sql statements
    # pre made statement to create recipes table
    sql_create_recipe_table_stmt = """CREATE TABLE IF NOT EXISTS
                                    recipes (
                                    recipe_id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    url text)"""
    #
    # pre made statement to create ingredients table
    sql_create_ingredients_table_stmt = """CREATE TABLE IF NOT EXISTS
                                            ingredients (
                                            ingredient_id integer PRIMARY KEY,
                                            name text NOT NULL)"""
    #
    # pre made statement to create recipe ingredient bridge table
    sql_create_recipe_ingredients_table_stmt = """CREATE TABLE IF NOT EXISTS
                                                recipe_ingredients(
                                                recipe_id integer,
                                                ingredient_id integer,
                                                FOREIGN KEY (recipe_id)
                                                REFERENCES recipes(recipe_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                                                FOREIGN KEY (ingredient_id)
                                                REFERENCES ingredients(ingredient_id)
                                                ON UPDATE CASCADE
                                                ON DELETE CASCADE
                                                );"""
    #
    # pre made sql statement to create temporary table with user input ingredients
    sql_create_user_ingredients_stmt = """CREATE TEMP TABLE user_ingredients (
                                        name text PRIMARY KEY
                                        )"""
    #
    # pre made sql statement to retreive recipes with listed ingredients
    sql_retrieve_recipes_stmt = """select ri.recipe_id from recipe_ingredients ri
                                inner join recipes r on ri.recipe_id = r.recipe_id
                                inner join ingredients i on i.ingredient_id = ri.ingredient_id
                                inner join user_ingredients ui on ui.name = i.name
                                group by ri.recipe_id
                                having count(*) = count(ui.name)
                                """
    #
    # prepared sql statement to insert data into ingredients table
    sql_populate_user_ingredients = "insert into user_ingredients (name) values (?)"
    #
    # prepared sql statement to insert data into recipes table
    sql_populate_recipes = "insert into recipes (name, url) values (?,?)"
    #
    # prepared sql statement to insert data into ingredients table
    sql_populate_ingredients = "insert into ingredients (name) values (?)"
    #
    # prepared sql statement to insert data into recipe_ingredients table
    sql_populate_recipe_ingredients = """insert into recipe_ingredients (recipe_id, ingredient_id)
                            values ((select recipe_id from recipes where name = ?),
                            (select ingredient_id from ingredients where name = ?))"""

    # The following are functions for secure database operation
    # init function for this class
    def __init__(self, db_file):
        """
        param db_file: location of db file to connect
        this init function will establish connection to database
        when the class is instantiated
        """
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)

    def create_user_ingreds_table(self):
        """
        this function creates the table to store user input ingredients
        """
        self.cur.execute(self.sql_create_user_ingredients_stmt)

    def populate_user_ingreds(self, user_list):
        """
        param user_list: array of ingredients supplied by user
        this function poulated the user_ingredients table
        """
        for i in user_list:
            self.cur.execute(self.sql_populate_user_ingredients, (i,))
        self.conn.commit()

    def create_recipes_table(self):
        """
        this function creates the table to store recipe data
        """
        self.cur.execute(self.sql_create_recipe_table_stmt)
        self.conn.commit()

    # the implementation of this function is likely to change as the project continues
    def populate_recipes(self, recipe_list):
        """
        param recipe_list: list of dictionaries with structure:
        {"recipe": "name", "ingredients": ["name1", "name2", "etc"], "url": "url_for_recipe"}
        this function populates the recipes table
        """
        for dictionary in recipe_list:
            recipe = None
            url = None
            for key, val in dictionary.items():
                if key == "recipe":
                    recipe = val
                if key == "url":
                    url = val
                if url is not None and recipe is not None:
                    self.cur.execute(self.sql_populate_recipes, (recipe, url))
        self.conn.commit()

    def create_ingredients_table(self):
        """
        this function creates the table to store ingredient data
        """
        self.cur.execute(self.sql_create_ingredients_table_stmt)
        self.conn.commit()

    # the implementation of this function is likely to change as the project continues
    def populate_ingredients(self, ingredients_list):
        """
        param: param ingredient_list: list of dictionaries with structure:
        {"recipe": "name", "ingredients": ["name1", "name2", "etc"], "url": "url_for_recipe"}
        this function populates the ingredients table
        """
        unique_ingreds = []
        for dictionary in ingredients_list:
            for key, val in dictionary.items():
                if key == "ingredients":
                    for item in val:
                        if item not in unique_ingreds:
                            unique_ingreds.append(item)

        for ingred in unique_ingreds:
            self.cur.execute(self.sql_populate_ingredients, (ingred,))
        self.conn.commit()

    def create_recipe_ingredients_table(self):
        """
        This function creates the bridge table recipe_ingredients
        """
        self.cur.execute(self.sql_create_recipe_ingredients_table_stmt)
        self.conn.commit()

    def populate_recipe_ingredients(self, recipe_dict):
        """
        param dict: list of dictionaries dictionary with basic structure:
        {"recipe": "name", "ingredients": ["name1", "name2", "etc"], "url": "url_for_recipe"}
        """
        recipe = None
        ingredient = None
        for dictionary in recipe_dict:
            for key, val in dictionary.items():
                if key != "url":
                    if key == "recipe":
                        recipe = val
                    if isinstance(val, list):
                        for item in val:
                            ingredient = item
                            self.cur.execute(
                                self.sql_populate_recipe_ingredients,
                                (recipe, ingredient),
                            )
        self.conn.commit()
