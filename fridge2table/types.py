"""Defines custom types/data structures"""
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Recipe:
    """Structure that contains recipe info"""

    name: str
    url: str
    image_url: str
    ingredients: list[str]

    def __str__(self):
        return str(self.to_dict)

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

    def to_dict(self) -> dict:
        """Convert recipe to a dictionary"""
        return {
            "name": self.name,
            "url": self.url,
            "image_url": self.image_url,
            "ingredients": self.ingredients,
        }
