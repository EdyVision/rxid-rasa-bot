# Utility Class for Drug Search Filtering and Response Formatting
from typing import Any, Text, Dict, List


def is_multiple_match(self, search_results):
    if len(search_results) > 1:
        return "There were {matches} matches for {name}."
    elif len(search_results) == 1:
        return "Found a match for {name}."
    elif len(search_results) == 0:
        return "There were no matches for {name}."
    else:
        return "The search was inconclusive."