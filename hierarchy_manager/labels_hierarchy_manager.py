from typing import Tuple, List, Optional
from itertools import chain, combinations
from utils.utils import get_lines_from_text_file
from utils.decorators import timing_decorator


class HierarchyManager:

    _hierarchy_separator = ' > '
    _words_to_ignore = ['and']

    def __init__(self, *, hierarchy_path: str):
        hierarchy = get_lines_from_text_file(hierarchy_path)
        self.hierarchy = self.parse_to_structure(hierarchy)

    def parse_to_structure(self, hierarchy: List[str]):
        raise NotImplementedError

    @timing_decorator
    def detect_labels(self, text: str) -> Tuple[List[str], List[str], Optional[str]]:
        """
        The function receives a string and extracts all of the labels that occur within the string.
        The function will return a tuple (extracted_labels, specific_labels, chosen_label) such that:

           - extracted_labels: all of the labels found in the string.

           - specific_labels: this list should contain all of the labels in extracted_labels that are NOT ancestors of other labels in extracted_labels.
                 For example, if extracted_labels = ["bakery", "cookies", "cakes"], then specific_labels = ["cookies", "cakes"] since bakery is the parent of cookies.

           - chosen_label: according to the following logic:
                 - If there is only one label in specific_labels, then chosen_label should be that label.
                 - Otherwise, if all of the labels in specific_labels have a common ancestor, then chosen_label will be their lowest common ancestor (LCA).
                 - In any other case, the field should contain None.

        Examples:
           - text = "yotpo"              =>   ( extracted_labels=[] , specific_labels=[], chosen_label=None )
           - text = "my tasty bread"     =>   ( extracted_labels=["bread"] , specific_labels=["bread"], chosen_label="bread" )
           - text = "board games"        =>   ( extracted_labels=["games", "board games"], specific_labels=["board games"], chosen_label="board games" )
           - text = "coffee and tea"     =>   ( extracted_labels=["coffee", "tea"], specific_labels=["coffee", "tea"], chosen_label="beverages" )
           - text = "cookies and candy"  =>   ( extracted_labels=["cookies", "candy"], specific_labels=["cookies", "candy"], chosen_label="food" )
           - text = "bread and water"    =>   ( extracted_labels=["bread", "water"], specific_labels=["bread", "water"], chosen_label=None )

        """
        search_labels = self.free_text_to_search_labels(text)

        extracted_labels, specific_labels = self.extract_labels(search_labels)

        if not specific_labels:
            chosen_label = None
        elif len(specific_labels) == 1:
            chosen_label = specific_labels[0]
        else:
            chosen_label = self.find_lca(specific_labels)

        return extracted_labels, specific_labels, chosen_label

    def free_text_to_search_labels(self, text: str) -> List[str]:
        text_list = [t for t in text.split(' ') if t not in self._words_to_ignore]
        subsets = list(chain.from_iterable(combinations(text_list, r) for r in range(len(text_list) + 1)))
        joined_subsets = [' '.join(s) for s in subsets if len(s) > 0]
        if text not in joined_subsets:
            joined_subsets.append(text)
        return joined_subsets

    def extract_labels(self, search_labels: List[str]) -> Tuple[List[str], List[str]]:
        raise NotImplementedError

    def find_lca(self, specific_labels: List[str]) -> str:
        raise NotImplementedError
