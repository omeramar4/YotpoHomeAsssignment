from tree_node import TreeNode
from typing import Union, Tuple, List, Optional


class HierarchyManager:

    _hierarchy_separator = ' > '

    def __init__(self, hierarchy: Union[str, TreeNode]):
        if type(hierarchy) == TreeNode:
            # TODO: validate input
            self.hierarchy = hierarchy
        elif type(hierarchy) == str:
            self.hierarchy = self.parse_hierarchy_text(hierarchy)

    def parse_hierarchy_text(self, hierarchy: str) -> TreeNode:
        try:
            with open(hierarchy, 'r') as f:
                lines = f.read().splitlines()
        except FileNotFoundError as e:
            raise e

        head = TreeNode('Head')

        for line in lines:
            labels = line.split(self._hierarchy_separator)
            head.insert_new_data(labels)

        return head

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
           - text = "board games"        =>   ( extracted_labels=["games", "board_games"], specific_labels=["board games"], chosen_label="board games" )
           - text = "coffee and tea"     =>   ( extracted_labels=["coffee", "tea"], specific_labels=["coffee", "tea"], chosen_label="beverages" )
           - text = "cookies and candy"  =>   ( extracted_labels=["cookies", "candy"], specific_labels=["cookies", "candy"], chosen_label="food" )
           - text = "bread and water"    =>   ( extracted_labels=["bread", "water"], specific_labels=["bread", "water"], chosen_label=None )

        """
        pass

    def find_lca(self, *args):
        pass