"""Recipe scraper prototype"""
import argparse
import itertools
import logging
import math
import multiprocessing
import os
from typing import Iterable

import PyIng
import recipe_scrapers
import requests
from bs4 import BeautifulSoup

TOTALLY_LEGIT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0."
)


def ingredient_list_to_search_sets(ingredients: Iterable[str]) -> list[tuple]:
    """Convert a list of ingredients into a collection of unique subsets for performing searches"""
    chain = itertools.chain.from_iterable(
        itertools.combinations(ingredients, r) for r in range(len(ingredients) + 1)
    )
    min_set_size = math.floor(math.sqrt(len(ingredients)))
    return [x for x in chain if len(x) >= min_set_size]


def search_epicurious(ingredients: Iterable[str]) -> set[str]:
    """Perform a recipe search on epicurious.com using the given ingredient list"""
    search_url = "https://www.epicurious.com/search/?include=" + "%2C".join(ingredients)
    logging.info("Getting %s ...", search_url)
    response = requests.get(
        search_url, headers={"User-Agent": TOTALLY_LEGIT_USER_AGENT}, timeout=30
    )

    if response.status_code != 200:
        logging.info("Got status code %d for %s", response.status_code, search_url)
        return set()

    soup = BeautifulSoup(response.content, "html.parser")
    return {
        "https://www.epicurious.com" + x["href"]
        for x in soup.select("a[href*='/recipes/food/views']")
    }


def scraped_recipe_to_dict(
    scraped_recipe: recipe_scrapers._abstract.AbstractScraper,
) -> dict:
    """Extract and cleanup relevant info from scraped recipe"""
    return {
        "name": scraped_recipe.title(),
        "url": scraped_recipe.canonical_url(),
        "image_url": scraped_recipe.image(),
        "ingredients": {
            x["name"]
            for x in PyIng.parse_ingredients(scraped_recipe.ingredients())
            if x["name"] != ""
        },
    }


def main() -> None:
    """Program entry point"""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i",
        "--ingredients",
        help="List of ingredients",
        nargs="+",
        required=True,
        metavar="INGREDIENT",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        help="Print verbose logs",
        action="store_true",
        required=False,
    )
    args = arg_parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    print("Searching for recipes...")
    search_sets = ingredient_list_to_search_sets(args.ingredients)
    urls = set()
    with multiprocessing.Pool() as p:
        urls.update(*p.map(search_epicurious, search_sets))
        raw_recipes = p.map(recipe_scrapers.scrape_me, urls)
        recipes = p.map(scraped_recipe_to_dict, raw_recipes)

    for recipe in recipes:
        print("Name:", recipe["name"])
        print("Link:", recipe["url"])
        print("Image URL:", recipe["image_url"])
        print("Ingredients:", recipe["ingredients"], os.linesep)


if __name__ == "__main__":
    main()
