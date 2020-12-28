from typing import Tuple, List, Optional
from itertools import chain, combinations
from utils.decorators import timing_decorator
from utils.utils import get_lines_from_text_file


class HierarchyManager:

    _hierarchy_separator = ' > '
    _distinction_word = 'and'

    def __init__(self, *, hierarchy_path: str):
        hierarchy = get_lines_from_text_file(hierarchy_path)
        self.hierarchy = self.parse_to_structure(hierarchy)
        self.industry_level = 1

    def parse_to_structure(self, hierarchy: List[str]):
        """
            Parse the text file to the correct data structure.

            :param hierarchy: A list of rows in the text file.
            :return: The data structure in ReturnType of inheritors.
        """
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
        """
            This functions gets free text and creates all possible subsets.

            :param text: Free text containing labels.

            :return: A list of the text itself and all possible subsets.
        """
        candidates = text.split(self._distinction_word)
        candidates = [c.strip() for c in candidates]

        joined_subsets = list()
        for c in candidates:
            text_list = [t for t in c.split(' ') if t not in self._distinction_word]
            subsets = list(chain.from_iterable(combinations(text_list, r) for r in range(len(text_list) + 1)))
            joined_subsets += [' '.join(s) for s in subsets if len(s) > 0]

        joined_subsets.append(text)
        return list(set(joined_subsets))        # prevent repeated elements

    def extract_labels(self, search_labels: List[str]) -> Tuple[List[str], List[str]]:
        """
            Extracts the labels from the list of subsets.

            :param search_labels: The labels to search.
            :return: A list of the extracted labels.
        """
        raise NotImplementedError

    def find_lca(self, specific_labels: List[str]) -> str:
        f"""
            Finds the LCA of all labels in {specific_labels}
            
            :param specific_labels: Labels for which the LCA is searched.
            :return: The LCA label.
        """
        raise NotImplementedError
