"""Defines custom types/data structures"""
from dataclasses import dataclass


@dataclass
class Recipe:
    """Structure that contains recipe info"""

    name: str
    url: str
    image_url: str
    ingredients: set[str]

    def __post_init__(self):
        if not isinstance(self.ingredients, set):
            self.ingredients = set(self.ingredients)

    def __str__(self):
        return str(
            {
                "name": self.name,
                "url": self.url,
                "image_url": self.image_url,
                "ingredients": self.ingredients,
            }
        )
