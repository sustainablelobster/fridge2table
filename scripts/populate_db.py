"""
Populates database using urls from csv file
"""

import logging
import csv
import recipe_scrapers
from fridge2table.types import Recipe, Ingredient
from fridge2table.db import DatabaseHandler

dbase = DatabaseHandler("fridge2table/populated_db.db")

# recipes = []

logging.basicConfig(
    filename="fridge2table/db_log/event_log.txt",
    format="%(asctime)s %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    filemode="a",
    level=logging.INFO,
)


def log_message(message=None):
    """
    This function utilizes the logger to log messages
    param message: message to be logged
    """
    if message is not None:
        logging.info(message)


def scraper_to_recipe(scraper) -> Recipe:
    """Borrowed from joe's scraper code
    Converts data from a scraped recipe to a Recipe object"""
    return Recipe(
        scraper.title(),
        scraper.canonical_url(),
        scraper.image(),
        {Ingredient(x) for x in scraper.ingredients()},
    )


with open(
    "prototypes/scraper/scrapy/epicurious/ \
    epicurious/csv_files/epicurious_recipe_urls.csv",
    "r",
    encoding="utf-8",
) as f:
    # read urls from csv file, scrape contents of web page, store relevent info in database

    datareader = csv.reader(f)
    for row in datareader:
        for url in row:
            try:
                dbase.add_recipe(scraper_to_recipe(recipe_scrapers.scrape_me(url)))
            except TypeError as e:
                print(f"{e}, recipe: {url} not added to db")
                log_message(f"{e}, recipe: {url} not added to db")
                continue
            except ValueError as e:
                log_message(f"{e}, recipe: {url} not added to db")
                print(f"{e}, recipe: {url} not added to db")
                continue
