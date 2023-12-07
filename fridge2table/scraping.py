"""Provides classes for scraping recipe websites"""
import logging
import multiprocessing
from abc import ABC, abstractmethod
from typing import Iterable

import recipe_scrapers
import requests
from bs4 import BeautifulSoup

from .types import Recipe
from .utils import powerset


class AbstractScraper(ABC):
    # pylint: disable=too-few-public-methods
    """Abstract base class which all recipe scrapers inherit from"""

    @classmethod
    def scrape(
        cls, ingredients: Iterable[str], known_urls: Iterable[str] = None
    ) -> set[Recipe]:
        """Takes a collection of Ingredients and returns a matching set of Recipes"""
        ingredients_powerset = powerset(ingredients)
        urls = set()
        with multiprocessing.Pool() as p:
            urls.update(*p.map(cls._search, ingredients_powerset))
            if known_urls is not None:
                urls -= set(known_urls)
            scrapers = p.map(recipe_scrapers.scrape_me, urls)
            return set(p.map(AbstractScraper._scraper_to_recipe, scrapers))

    @classmethod
    def _scraper_to_recipe(
        cls, scraper: recipe_scrapers._abstract.AbstractScraper
    ) -> Recipe:
        """Converts data from a scraped recipe to a Recipe object"""
        return Recipe(
            scraper.title(),
            scraper.canonical_url(),
            scraper.image(),
            scraper.ingredients(),
        )

    @classmethod
    @abstractmethod
    def _search(cls, ingredients: set[str]) -> set[str]:
        """Search for recipes that match the given set of Ingredients"""


class EpicuriousScraper(AbstractScraper):
    # pylint: disable=too-few-public-methods
    """Recipe scraper for epicurious.com"""

    _USER_AGENT = (
        "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0."
    )

    @classmethod
    def _search(cls, ingredients: set[str]) -> set[str]:
        """Search epicurious.com for recipes that match the given set of Ingredients"""
        search_url = "https://www.epicurious.com/search/?include=" + "%2C".join(
            ingredients
        )
        logging.info("Getting %s ...", search_url)

        response = requests.get(
            search_url,
            headers={"User-Agent": cls._USER_AGENT},
            timeout=30,
        )

        if response.status_code != 200:
            logging.info("Got status code %d for %s", response.status_code, search_url)
            return set()

        soup = BeautifulSoup(response.content, "html.parser")
        return {
            "https://www.epicurious.com" + x["href"]
            for x in soup.select("a[href*='/recipes/food/views']")
        }
