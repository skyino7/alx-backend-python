#!/usr/bin/env python3
"""
Annotate the below function’s parameters and
return values with the appropriate types
"""

from typing import List, Sequence, Iterable, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Annotated Function
    """
    return [(i, len(i)) for i in lst]
