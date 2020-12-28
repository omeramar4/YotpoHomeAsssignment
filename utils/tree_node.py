from operator import is_not
from functools import reduce, partial
from typing import List, Set, Dict, Union, Optional
from utils.utils import number_of_appeared_elements


class TreeNode:

    def __init__(self, data: str):
        self.data = data
        self.children = list()

    def add_child(self, child_data: 'TreeNode'):
        self.children.append(child_data)

    def get_children_data(self) -> List[str]:
        """
            Gets the data appear in the next level.

            :return: A list of the data in the node's children.
        """
        return [child.data for child in self.children]

    def get_children_data_by_level(self, level: int) -> Set[str]:
        """
            Gets the data appear in the {level} next levels.

            :param level: The number of levels from which data is received.
            :return: A set of all the data in the node and it's {level} bottom levels.
        """
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
        """
            Gets child instance by key.

            :param data: The data to search in the instance's children.
            :return: TreeNode instance that in which the data is stored.
        """
        return self.children[self.get_children_data().index(data)]

    def insert_new_data(self, path: List[str]):
        """
            Gets a path to a label and insert it to the tree.

            :param path: A list of the labels on the path.
        """
        children_data = self.get_children_data()
        if len(path) == 1 and path not in children_data:
            self.add_child(TreeNode(path[0]))
            return

        if path[0] not in children_data:
            self.add_child(TreeNode(path[0]))
            next_node = self.children[-1]
        else:
            next_node = self.get_child_by_data(path[0])

        next_node.insert_new_data(path[1:])

    def get_all_data(self) -> Set[str]:
        """
            Gets all data in the tree including leaves.

            :return: A set of all data in the tree.
        """
        if not self.children:
            return {self.data}

        children_data = set()
        for child in self.children:
            children_data = children_data.union(child.get_all_data())

        children_data.add(self.data)
        return children_data

    def get_all_data_by_child(self) -> List[Set[str]]:
        """
            Gets all data in the tree, divided by children.

            :return: A list of sets of all data by children.
        """
        children_data = list()
        for child in self.children:
            children_data.append(child.get_all_data())
        return children_data

    def get_all_data_with_distinction(self, return_value: Dict[bool, Set[str]] = None
                                      ) -> Dict[bool, Set[str]]:
        """
            Gets all data in the tree with distinction of which label is a leaf.

            :param return_value: The updated dictionary that goes through the recursion levels
            :return: A dictionary of all data in the following format:
                     {True: {leaves data}, False: {non-leaves data}}
        """
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
        """
            Gets all data in the tree with distinction of which label is a leaf.

            :param return_value: The updated dictionary that goes through the recursion levels
            :return: A dictionary of all data in the following format:
                     {data: {True if leaf else False}}
        """
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

    def find_lca_original(self, labels: List[str]) -> Union[Optional[str], int]:
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

    # This function returns pointer to LCA of two given
    # values n1 and n2
    # This function assumes that n1 and n2 are present in
    # Binary Tree
    def find_lca(self, labels: List[str]):
        if True in [self.data == label for label in labels]:
            return self

        if not self.children:
            return None

        children_lca = [child.find_lca(labels) for child in self.children]

        if len(children_lca) == 1 and children_lca[0] is not None:
            return children_lca[0]

        if reduce(lambda c1, c2: c1 and c2, children_lca):
            return self

        lca_child = list(filter(partial(is_not, None), children_lca))
        if not lca_child:
            return None

        if len(lca_child) == len(labels):
            return self

        return lca_child[0]
