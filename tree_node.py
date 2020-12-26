from typing import List


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
