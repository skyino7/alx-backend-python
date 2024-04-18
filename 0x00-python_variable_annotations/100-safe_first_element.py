#!/usr/bin/env python3
"""Augment the following code with the
correct duck-typed annotations:"""

from typing import Union, Any, Sequence


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return the first element, or otherwise None"""
    if lst:
        return lst[0]
    else:
        return None
