import pandas as pd
from typing import Tuple, List, Optional, Set
from pandas import DataFrame as PandasDataFrame
from hierarchy_manager.labels_hierarchy_manager import HierarchyManager


class DataFrameHierarchyManager(HierarchyManager):

    ReturnType = PandasDataFrame

    def __init__(self, *, hierarchy_path: str):
        super().__init__(hierarchy_path=hierarchy_path)
        self.na_value = ''
        self.specific_rows = None

    def parse_to_structure(self, hierarchy: List[str]) -> ReturnType:
        max_length = max(map(lambda e: e.count(self._hierarchy_separator), hierarchy))
        lines_with_nulls = list(map(lambda e: (e + (self._hierarchy_separator *
                                                    (max_length - e.count(self._hierarchy_separator)))
                                               ).split(self._hierarchy_separator),
                                    hierarchy))
        return pd.DataFrame(lines_with_nulls)

    def find_rows_by_labels(self, labels: List[str]) -> Tuple[PandasDataFrame, Set[str]]:
        num_of_cols = len(self.hierarchy.columns)
        rows_found = list()
        labels_to_find = set(labels)

        for col in reversed(range(num_of_cols)):
            rows = self.hierarchy[self.hierarchy[col].isin(labels_to_find)]
            if col < num_of_cols - 1:
                rows = rows[rows[col + 1] == self.na_value]
            rows_found.append(rows)
            labels_found = set(rows[col].unique())
            labels_to_find -= labels_found
            if not labels_to_find:
                break

        selected_rows = pd.concat(rows_found)
        self.specific_rows = selected_rows
        return selected_rows, labels_to_find

    def extract_labels(self, search_labels: List[str]) -> Tuple[List[str], List[str]]:
        selected_rows, remaining_labels = self.find_rows_by_labels(search_labels)
        extracted_labels = list(set(search_labels) - remaining_labels)

        specific_labels = self.get_specific_labels(extracted_labels)

        return extracted_labels, specific_labels

    def get_specific_labels(self, extracted_labels: List[str]) -> List[str]:
        specific_labels = list()
        num_of_cols = len(self.hierarchy.columns)
        for label in extracted_labels:
            if self.hierarchy[num_of_cols - 1].str.contains(label).any():
                specific_labels.append(label)
                continue
            for col in reversed(range(num_of_cols - 1)):
                mask = self.hierarchy[self.hierarchy[col] == label]
                if mask.empty:
                    continue
                num_of_nulls = sum(mask[col + 1] != self.na_value)
                if not num_of_nulls:
                    specific_labels.append(label)
                break
        return specific_labels

    def find_lca(self, specific_labels: List[str]) -> Optional[str]:
        if self.specific_rows is None:
            self.find_rows_by_labels(specific_labels)

        no_null_cols = self.specific_rows[self.specific_rows != self.na_value]
        no_null_cols.dropna(axis=1, inplace=True)
        constant_cols = list(no_null_cols.columns[no_null_cols.nunique() <= 1])
        if len(constant_cols) <= 1:
            return None
        return no_null_cols.iloc[0][constant_cols[-1]]


if __name__ == '__main__':
    x = DataFrameHierarchyManager(hierarchy_path='/Users/oamar/Documents/Interviews/YotpoHomeAsssignment/data/hierarchy.txt')
    a, b, c = x.detect_labels('yotpo')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels('my tasty bread')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels('board games')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels('coffee and tea')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels('cookies and candy')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels('bread and water')
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
    a, b, c = x.detect_labels("bakery and cookies omer amar cakes")
    print(f'extracted labels: {a}, specific labels: {b}, chosen label: {c}')
