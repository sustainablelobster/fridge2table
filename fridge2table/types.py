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
