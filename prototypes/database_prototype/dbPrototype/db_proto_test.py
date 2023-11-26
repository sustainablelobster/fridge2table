"""
importing python class that handles db operation
this python program is used exclusively to test DbProto
"""
import db_proto as db
import csv
import recipe_scrapers
import PyIng
from sqlite3 import OperationalError
import logging
import datetime
import pandas as pd

logging.basicConfig(filename="prototypes/database_prototype/dbPrototype/event_log.txt",
                    format="%(asctime)s %(levelname)s : %(message)s",
                    datefmt="%Y-%m-%d %H:%M",
                    filemode="a",
                    level=logging.INFO)

def log_message(message=None):
    """
    This function utilizes the logger to log messages
    param message: message to be logged
    """
    if message is not None:
        logging.info(message)

"""
Stolen from joe's scraper prototype
"""
def scraped_recipe_to_dict(
    scraped_recipe: recipe_scrapers._abstract.AbstractScraper,
) -> dict:
    """Extract and cleanup relevant info from scraped recipe"""
    return {
        "recipe": scraped_recipe.title(),
        "url": scraped_recipe.canonical_url(),
        "image_url": scraped_recipe.image(),
        "ingredients": [x["name"] for x in PyIng.parse_ingredients(scraped_recipe.ingredients()) if x["name"] != ""
        ],
    }

#
# user_list = ["chicken", "peas", "rice"]

dbOps = db.DbProto("prototypes/database_prototype/protoDB.db")

# try:
#     dbOps.cur.execute("drop table recipes")
# except OperationalError:
#     print("recipes already dropped")

# try:
#     dbOps.cur.execute("drop table ingredients")
# except OperationalError:
#     print("recipes already dropped")
# try:
#     dbOps.cur.execute("drop table recipe_ingredients")
# except OperationalError:
#     print("recipes already dropped")

# dbOps.conn.commit()
# print("done")
dbOps.cur.execute(dbOps.sql_create_recipe_table_stmt)
dbOps.cur.execute(dbOps.sql_create_ingredients_table_stmt)
dbOps.cur.execute(dbOps.sql_create_recipe_ingredients_table_stmt)
dbOps.cur.execute(dbOps.sql_create_user_ingredients_stmt)

"""
Dont run this code
Don't delete this code, I will need to reference it later
"""

# file = "prototypes/scraper/scrapy/epicurious/epicurious/csv_files/epicurious_recipe_urls.csv"

# recipes = []
# count = 0
# started = datetime.datetime.now()
# date_time_format = started.strftime("%m/%d/%Y %H:%M")
# log_message(f"Started at {date_time_format}")
# with open(file, "r") as f:
#     datareader = csv.reader(f)
#     for row in datareader:
#         for url in row:
#             try:
#                 recipe_dict = scraped_recipe_to_dict(recipe_scrapers.scrape_me(url))
#                 recipes.append(recipe_dict)
#                 print(count)
#                 count+=1
#             except TypeError as e:
#                 print(f"{e}, recipe: {url} not added to db")
#                 log_message(f"{e}, recipe: {url} not added to db")
#                 continue
#             except ValueError as e:
#                 log_message(f"{e}, recipe: {url} not added to db")
#                 print(f"{e}, recipe: {url} not added to db")
#                 continue
#             except Exception as e:
#                 log_message(f"{e}, recipe: {url} not added to db")
#                 continue

# try:
#     dbOps.populate_ingredients(recipes)
#     dbOps.populate_recipes(recipes)
#     dbOps.populate_recipe_ingredients(recipes)
#     dbOps.conn.commit()
#     print("done")
# except OperationalError as e:
#     print(f"Operational error {e}")
#     log_message(f"{e}, db not populated")


# finished = datetime.datetime.now()
# date_time_format = finished.strftime("%m/%d/%Y %H:%M")
# log_message(f"Finished at {date_time_format}")

"""
Safe to run past this point
"""

print("select recipe test")
dbOps.cur.execute("select * from recipes")
for i in dbOps.cur.fetchall():
    print(i)
# print("select ingredient test")
# dbOps.cur.execute("select * from ingredients")
# for i in dbOps.cur.fetchall():
#     print(i)
print("select recipe ingredient test")
dbOps.cur.execute("select recipe_id, ingredient_id from recipe_ingredients where recipe_id = 10375")
for i in dbOps.cur.fetchall():
   print(i)

# def main():
#     """
#     main function
#     """
#     # create all tables
#     dbOps.cur.execute(dbOps.sql_create_recipe_table_stmt)
#     dbOps.cur.execute(dbOps.sql_create_ingredients_table_stmt)
#     dbOps.cur.execute(dbOps.sql_create_recipe_ingredients_table_stmt)
    #dbOps.cur.execute(dbOps.sql_create_user_ingredients_stmt)

#     # populate tables with data
#     dbOps.populate_recipes(recipe_dict)
#     dbOps.populate_ingredients(recipe_dict)
#     dbOps.populate_recipe_ingredients(recipe_dict)
# dbOps.populate_user_ingreds(user_list)

#     # queries
#     dbOps.cur.execute("select * from recipes")
#     for i in dbOps.cur.fetchall():
#         print(i)
#     print("\n")
#     dbOps.cur.execute("select * from ingredients")
#     for i in dbOps.cur.fetchall():
#         print(i)
#     print("\n")
#     dbOps.cur.execute("select * from recipe_ingredients")
#     for i in dbOps.cur.fetchall():
#         print(i)
#     print("\n")
# print("retrieve recipes test")
# dbOps.cur.execute(dbOps.sql_retrieve_recipes_stmt)
# for i in dbOps.cur.fetchall():
#     print(i)




# main()
