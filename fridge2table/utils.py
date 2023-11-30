"""Miscellaneous utility functions"""
import itertools
from typing import Iterable


def powerset(iterable: Iterable, exclude_empty: bool = True) -> set[frozenset]:
    """Returns a powerset (set of all sets) for the given collection"""
    chain = itertools.chain.from_iterable(
        itertools.combinations(iterable, r) for r in range(len(iterable) + 1)
    )
    ret_val = {frozenset(x) for x in chain}
    if exclude_empty:
        ret_val.remove(set())
    return ret_val


def dedup_list(l: list) -> list:
    """Remove duplicate items from list"""
    return list(set(l))
