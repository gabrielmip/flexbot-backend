import itertools
from typing import List


def flatten(list_of_lists: List[List]):
    return itertools.chain(*list_of_lists)
