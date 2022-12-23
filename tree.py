class Node:

    def __init__(self) -> None:
        self.parent = None
        self.children = []

    def append_child(self, node):
        if node is not Node:
            raise Exception("Type must be Node")
        else:
            self.children.append(node)

    def remove_child(self, node):
        self.children.remove(node)

    def get_value(self):
        pass

    def get_parent(self):
        return self.parent


class Tree:
    root: Node

    def __init__(self, node) -> None:
        self.root = node

    def preorder_node(self, node: Node, callback):
        result = callback(node)
        for child in node.children:
            self.preorder_node(child, callback)

        return result

    def preorder_traversal(self, callback):
        if self.root is None:
            return None
        result = self.preorder_node(self.root, callback)





