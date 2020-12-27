import pandas as pd
from pandas import DataFrame as PandasDataFrame
from typing import Union, Tuple, List, Optional, Dict, Set
from hierarchy_manager.labels_hierarchy_manager import HierarchyManager


class DataFrameHierarchyManager(HierarchyManager):

    ReturnType = PandasDataFrame

    def __init__(self, *, hierarchy_path: str):
        super().__init__(hierarchy_path=hierarchy_path)

    def parse_to_structure(self, hierarchy: List[str]) -> ReturnType:
        max_length = max(map(lambda e: e.count(self._hierarchy_separator), hierarchy))
        lines_with_nulls = list(map(lambda e: (e + (self._hierarchy_separator *
                                                    (max_length - e.count(self._hierarchy_separator)))
                                               ).split(self._hierarchy_separator),
                                    hierarchy))
        return pd.DataFrame(lines_with_nulls)

    def extract_labels(self, search_labels: List[str]) -> Tuple[List[str], List[str]]:
        num_of_cols = len(self.hierarchy.columns)
        dfs = []
        labels_to_find = set(search_labels)

        for col in reversed(range(num_of_cols)):
            rows = self.hierarchy[self.hierarchy[col].isin(labels_to_find)]
            dfs.append(rows)
            labels_found = set(rows[col].unique())
            labels_to_find -= labels_found
            if not labels_to_find:
                break

        selected_rows = pd.concat(dfs)
        extracted_labels = list(set(search_labels) - labels_to_find)
        specific_labels = list(selected_rows.apply(lambda row: row[row.last_valid_index()], axis=1))

        return extracted_labels, specific_labels

    def find_lca(self, specific_labels: List[str]) -> Optional[str]:
        chosen_label = self.hierarchy.find_lca(specific_labels)
        if chosen_label in self.hierarchy.get_children_data():
            chosen_label = None
        return chosen_label


if __name__ == '__main__':
    import os
    path = '/Users/oamar/Documents/Interviews/YotpoHomeAsssignment/data/hierarchy.txt'
    pd_hierarchy = DataFrameHierarchyManager(hierarchy_path=path)
    # search_labels = ['omer']
    # search_labels = ['cookies', 'candy']
    search_labels = ['games', 'board games']
    # search_labels = ['bread']
    # search_labels = ['coffee', 'tea']
    # search_labels = ['berad', 'water']
    num_of_cols = len(pd_hierarchy.hierarchy.columns)
    dfs = []
    labels_to_find = set(search_labels)

    for col in reversed(range(num_of_cols)):
        rows = pd_hierarchy.hierarchy[pd_hierarchy.hierarchy[col].isin(labels_to_find)]
        dfs.append(rows)
        labels_found = set(rows[col].unique())
        labels_to_find -= labels_found
        if not labels_to_find:
            break

    selected_rows = pd.concat(dfs)
    extracted_labels = set(search_labels) - labels_to_find
    print('')