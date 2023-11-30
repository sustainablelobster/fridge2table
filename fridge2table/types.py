"""Defines custom types/data structures"""
import logging
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

import PyIng
from pluralizer import Pluralizer


@dataclass
class Ingredient:
    """Structure that contains normalized Ingredient name"""

    name: str

    def __post_init__(self):
        self.name = self._normalize(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def _normalize(name: str) -> str:
        """Extract ingredient name from raw string and convert to singular form"""
        if name is None:
            return None

        try:
            parsed_name = PyIng.parse_ingredients(name)["name"]
        except ValueError:
            parsed_name = None

        if parsed_name == "" or parsed_name is None:
            logging.error("Unable to parse ingredient from string: '%s'", name)
            return None

        return Pluralizer().singular(parsed_name)


@dataclass
class Recipe:
    """Structure that contains recipe info"""

    name: str
    url: str
    image_url: str
    ingredients: list[str]

    def __str__(self):
        return str(
            {
                "name": self.name,
                "url": self.url,
                "image_url": self.image_url,
                "ingredients": self.ingredients,
            }
        )

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.url == other.url
            and self.image_url == other.image_url
            and Counter(self.ingredients) == Counter(other.ingredients)
        )

    def __hash__(self):
        return hash(str(self))

    def rank(self, ingredients: Iterable[str]) -> float:
        """Get the ratio of matching ingredients to total ingredients in recipe"""
        matches = 0
        for ingredient in ingredients:
            for recipe_ingredient in self.ingredients:
                if ingredient in recipe_ingredient:
                    matches += 1
                    break
        return matches / len(self.ingredients)
