import ast
from collections import defaultdict

class CFGNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.lineno = None
        self.type = None

    def add_child(self, node):
        self.children.append(node)

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.cfg = []
        self.node_stack = []
        self.current_node = None

    def push_node(self, node):
        self.node_stack.append(node)
        self.current_node = node

    def pop_node(self):
        self.node_stack.pop()
        if len(self.node_stack) > 0:
            self.current_node = self.node_stack[-1]
        else:
            self.current_node = None

    def visit(self, node):
        super().visit(node)
        self.pop_node()

    def generic_visit(self, node):
        new_node = CFGNode(self.current_node)
        new_node.lineno = getattr(node, "lineno", None)
        new_node.type = node.__class__.__name__
        if self.current_node is not None:
            self.current_node.add_child(new_node)
        self.push_node(new_node)
        super().generic_visit(node)

    def build_cfg(self, node):
        self.push_node(CFGNode())
        self.visit(node)

        cfg = defaultdict(list)
        for node in self.cfg:
            if node.parent is not None:
                cfg[node.parent].append(node)

        return cfg
