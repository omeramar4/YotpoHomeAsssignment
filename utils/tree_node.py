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

    def get_child_by_data(self, data: str) -> 'TreeNode':
        return self.children[self.get_children_data().index(data)]

    def insert_new_data(self, row: List[str], node: 'TreeNode' = None):
        node = node or self
        children_data = node.get_children_data()
        if len(row) == 1 and row not in children_data:
            node.add_child(TreeNode(row[0]))
            return

        if row[0] not in children_data:
            node.add_child(TreeNode(row[0]))
            next_node = node.children[-1]
        else:
            next_node = node.get_child_by_data(row[0])

        self.insert_new_data(row[1:], next_node)

    def get_all_data(self, node: 'TreeNode' = None) -> Set[str]:
        node = node or self
        if not node.children:
            return {node.data}

        children_data = set()
        for child in node.children:
            children_data = children_data.union(self.get_all_data(child))

        children_data.add(node.data)
        return children_data

    def get_all_data_by_child(self) -> List[Set[str]]:
        children_data = list()
        for child in self.children:
            children_data.append(self.get_all_data(child))
        return children_data

    def get_all_data_with_distinction(self, node: 'TreeNode' = None,
                                      return_value: Dict[bool, Set[str]] = None
                                      ) -> Dict[bool, Set[str]]:
        node = node or self

        if return_value is not None and False in return_value.keys():
            return_value[False].add(node.data)
        if return_value is None:
            return_value = {False: {node.data}}

        for child in node.children:
            if not child.children:
                if True in return_value.keys():
                    return_value[True].add(child.data)
                else:
                    return_value[True] = {child.data}
                continue
            child_data = self.get_all_data_with_distinction(child, return_value)
            if True in return_value.keys():
                return_value[True] = return_value[True].union(child_data[True])
            else:
                return_value[True] = child_data[True]
            return_value[False] = return_value[False].union(child_data[False])

        return return_value

    def get_all_data_with_distinction_label_as_key(self, node: 'TreeNode' = None
                                                   ) -> Dict[str, bool]:
        node = node or self
        if not node.children:
            return {node.data: True}

        all_data = {node.data: False}
        for child in node.children:
            all_data.update(self.get_all_data_with_distinction_label_as_key(child))

        return all_data

    def find_lca(self, labels: List[str], node: 'TreeNode' = None, already_found: int = 0) -> Union[Optional[str], int]:
        node = node or self
        num_of_elements = number_of_appeared_elements(labels, list(self.get_all_data(node)))
        if 0 < num_of_elements < len(labels):
            return num_of_elements

        if num_of_elements == len(labels):
            for child in node.children:
                child_data = self.find_lca(labels, child, already_found)
                if isinstance(child_data, int):
                    already_found += child_data
                if already_found == len(labels):
                    return node.data
                if isinstance(child_data, str):
                    return child_data
        else:
            return 0

        return None

    def find_lca2(self, labels: List[str], node: 'TreeNode' = None, already_found: int = 0) -> Union[Optional[str], int]:
        node = node or self
        children_data = node.get_all_data_by_child()
        num_of_elements_found = 0
        selected_child = None
        for child, child_data in zip(node.children, children_data):
            num_of_elements = number_of_appeared_elements(labels, list(child_data))
            if num_of_elements == len(labels):
                selected_child = child
                break
            elif 0 < num_of_elements < len(labels):
                num_of_elements_found += num_of_elements

        if selected_child is not None:
            return self.find_lca2(labels, selected_child, already_found)

        elif num_of_elements_found == len(labels):
            return node.data

        return None