from typing import Iterable, Set, TypeVar

from functools import reduce
from itertools import chain

T = TypeVar("T")


def intersection(items: Iterable[Iterable[T]]) -> Set[T]:
    """Does an intersection over all collection of items

    Parameters
    ----------
    items : Iterable[Iterable[T]]
        A list of lists


    Returns
    -------
    Set[T]
        The intersection of all items
    """
    return set(reduce(lambda s1, s2: set(s1) & set(s2), items))


def union(items: Iterable[Iterable[T]]) -> Set[T]:
    """Does a union over all collection of items

    Parameters
    ----------
    items : Iterable[Iterable[T]]
        A list of lists

    Returns
    -------
    Set[T]
        The intersection of all items
    """
    return set(chain.from_iterable(items))
