from utils.tree_node import TreeNode
from typing import List, Tuple, Optional
from hierarchy_manager.labels_hierarchy_manager import HierarchyManager


class TreeHierarchyManager(HierarchyManager):

    ReturnType = TreeNode

    def __init__(self, *, hierarchy_path: str):
        super().__init__(hierarchy_path=hierarchy_path)

    def parse_to_structure(self, hierarchy: List[str]) -> ReturnType:
        head = TreeNode('Head')

        for line in hierarchy:
            labels = line.split(self._hierarchy_separator)
            head.insert_new_data(labels)

        return head

    def extract_labels(self, search_labels: List[str]) -> Tuple[List[str], List[str]]:

        all_data = self.hierarchy.get_all_data_with_distinction()

        # Dict[bool, Set[str]]
        extracted_labels = [s for s in search_labels if s in all_data[True].union(all_data[False])]
        specific_labels = [s for s in extracted_labels if s in all_data[True]]

        # Dict[str, bool]
        # extracted_labels = [s for s in joined_subsets if s in all_data.keys()]
        # specific_labels = [s for s in extracted_labels if all_data[s]]

        return extracted_labels, specific_labels

    def find_lca(self, specific_labels: List[str]) -> Optional[str]:
        chosen_label = self.hierarchy.find_lca(specific_labels)
        if chosen_label in self.hierarchy.get_children_data():
            chosen_label = None
        return chosen_label
