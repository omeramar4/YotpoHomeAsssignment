from functools import reduce
from typing import List, Set, Dict, Union, Optional
from utils.utils import number_of_appeared_elements


class TreeNode:

    def __init__(self, data: str):
        self.data = data
        self.children = list()

    def add_child(self, child_data: 'TreeNode'):
        self.children.append(child_data)

    def get_children_data(self) -> List[str]:
        return [child.data for child in self.children]

    def get_children_data_by_level(self, level: int,):
        if level == 0:
            return {self.data}
        elif level == 1:
            return_data = set(self.get_children_data())
            return_data.add(self.data)
            return return_data

        data = {self.data}
        for child in self.children:
            data = data.union(child.get_children_data_by_level(level - 1))

        return data

    def get_child_by_data(self, data: str) -> 'TreeNode':
        return self.children[self.get_children_data().index(data)]

    def insert_new_data(self, row: List[str]):
        children_data = self.get_children_data()
        if len(row) == 1 and row not in children_data:
            self.add_child(TreeNode(row[0]))
            return

        if row[0] not in children_data:
            self.add_child(TreeNode(row[0]))
            next_node = self.children[-1]
        else:
            next_node = self.get_child_by_data(row[0])

        next_node.insert_new_data(row[1:])

    def get_all_data(self) -> Set[str]:
        if not self.children:
            return {self.data}

        children_data = set()
        for child in self.children:
            children_data = children_data.union(child.get_all_data())

        children_data.add(self.data)
        return children_data

    def get_all_data_by_child(self) -> List[Set[str]]:
        children_data = list()
        for child in self.children:
            children_data.append(child.get_all_data())
        return children_data

    def get_all_data_with_distinction(self, return_value: Dict[bool, Set[str]] = None
                                      ) -> Dict[bool, Set[str]]:
        if return_value is not None and False in return_value.keys():
            return_value[False].add(self.data)
        if return_value is None:
            return_value = {False: {self.data}}

        for child in self.children:
            if not child.children:
                if True in return_value.keys():
                    return_value[True].add(child.data)
                else:
                    return_value[True] = {child.data}
                continue
            child_data = child.get_all_data_with_distinction(return_value)
            if True in return_value.keys():
                return_value[True] = return_value[True].union(child_data[True])
            else:
                return_value[True] = child_data[True]
            return_value[False] = return_value[False].union(child_data[False])

        return return_value

    def get_all_data_with_distinction_label_as_key(self) -> Dict[str, bool]:
        if not self.children:
            return {self.data: True}

        all_data = {self.data: False}
        for child in self.children:
            all_data.update(child.get_all_data_with_distinction_label_as_key())

        return all_data

    def find_lca_backup(self, labels: List[str], already_found: int = 0
                        ) -> Union[Optional[str], int]:
        num_of_elements = number_of_appeared_elements(labels, list(self.get_all_data()))
        if 0 < num_of_elements < len(labels):
            return num_of_elements

        if num_of_elements == len(labels):
            for child in self.children:
                child_data = child.find_lca_backup(labels, already_found)
                if isinstance(child_data, int):
                    already_found += child_data
                if already_found == len(labels):
                    return self.data
                if isinstance(child_data, str):
                    return child_data
        else:
            return 0

        return None

    def find_lca(self, labels: List[str]) -> Union[Optional[str], int]:
        children_data = self.get_all_data_by_child()
        num_of_elements_found = 0
        selected_child = None
        for child, child_data in zip(self.children, children_data):
            num_of_elements = number_of_appeared_elements(labels, list(child_data))
            if num_of_elements == len(labels):
                selected_child = child
                break
            elif 0 < num_of_elements < len(labels):
                num_of_elements_found += num_of_elements

        if selected_child is not None:
            return selected_child.find_lca(labels)

        elif num_of_elements_found == len(labels):
            return self.data

        return None
