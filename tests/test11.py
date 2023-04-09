from typing import List, Dict
from collections import defaultdict
from phply import phpast as php

global block_id

block_id=0


def get_new_block_id():
    #label id定义
    global block_id
    block_id += 1
    return f'b{block_id}'

class CFGNode:
    def __init__(self, ast_node):
        self.label=get_new_block_id()
        self.ast_node =ast_node
        self.parents = []
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)
        
class CFG:
    def __init__(self, ast_root):
        self.ast_root = ast_root
        self.nodes = {}
        self._build_cfg(ast_root)
        
    def _build_cfg(self, ast_node):
        node = CFGNode(ast_node)
        self.nodes[node.label] = node
        
        if isinstance(ast_node, (php.Block, php.Function, php.Method, php.Closure, php.Try, php.Catch, php.Finally, php.Class, php.Trait)):
            last_node = None
            for n in ast_node.nodes:
                child_node = self._build_cfg(n)
                if last_node is not None:
                    last_node.add_child(child_node)
                last_node = child_node
        elif isinstance(ast_node, php.If):
            cond_node = self._build_cfg(ast_node.expr)
            node.add_child(cond_node)
            
            last_node = cond_node
            for n in ast_node.node:
                child_node = self._build_cfg(n)
                last_node.add_child(child_node)
                last_node = child_node
                
            if ast_node.elseifs:
                for elseif in ast_node.elseifs:
                    elseif_node = self._build_cfg(elseif)
                    last_node.add_child(elseif_node)
                    last_node = elseif_node
                    
            if ast_node.else_:
                else_node = self._build_cfg(ast_node.else_)
                last_node.add_child(else_node)
        elif isinstance(ast_node, php.ElseIf):
            cond_node = self._build_cfg(ast_node.expr)
            node.add_child(cond_node)
            
            last_node = cond_node
            for n in ast_node.node:
                child_node = self._build_cfg(n)
                last_node.add_child(child_node)
                last_node = child_node
        elif isinstance(ast_node, php.Else):
            last_node = None
            for n in ast_node.node:
                child_node = self._build_cfg(n)
                if last_node is not None:
                    last_node.add_child(child_node)
                last_node = child_node
        elif isinstance(ast_node, php.While):
            cond_node = self._build_cfg(ast_node.expr)
            node.add_child(cond_node)
            
            body_node = self._build_cfg(ast_node.node)
            cond_node.add_child(body_node)
            body_node.add_child(cond_node)
            
            if ast_node.next is not None:
                next_node = self._build_cfg(ast_node.next)
                body_node.add_child(next_node)
                next_node.add_child(cond_node)
        elif isinstance(ast_node,php.DoWhile):
            body_node = self._build_cfg(ast_node.node)
            node.add_child(body_node)
            
            cond_node = self._build_cfg(ast_node.expr)
            body_node.add_child(cond_node)
            cond_node.add_child(body_node)
            
            if ast_node.next is not None:
                next_node = self._build_cfg(ast_node.next)
                body_node.add_child(next_node)
                next_node.add_child(cond_node)
        elif isinstance(ast_node, php.For):
            if ast_node.start is not None:
                start_node = self._build_cfg(ast_node.start)
                node.add_child(start_node)
                
                cond_node = self._build_cfg(ast_node.test)
                start_node.add_child(cond_node)
            else:
                cond_node = self._build_cfg(ast_node.test)
                node.add_child(cond_node)
            
            body_node = self._build_cfg(ast_node.node)
            cond_node.add_child(body_node)
            body_node.add_child(cond_node)
            
           
# def new_variable():
#     #返回一个新变量名，同时更新全局计数器
#     global variable_id
#     variable_id += 1
#     return f"v{variable_id}"


# def node_type(node):
#     #一个节点的类型
#     return type(node).__name__

# def is_node_type(node, type_):
#     #判断一个节点是否是指定类型
#     return node_type(node) == type_


# def new_block():
#     #创建基本块
#     global block_id
#     block_id += 1
#     return Block(f"b{block_id}", [])

# def connect_blocks(block1, block2):
#     #连接两个基本块
#     #'new_blockblock_id。'connect_blocksconnect_blocks函数将第一个基本块连接到第二个基本块，并在第一个基本块的节点列表中添加一个跳转指令。
#     block1.nodes.append(Goto(block2.name))
#     block2.predecessors.append(block1)


# def add_node(block, node):
#     #指定基本块中添加节点的函数
#     block.nodes.append(node)
#     node.block = block


# def to_cfg(node):

#     """
#     Convert an AST node to the corresponding CFG node.
#     """
#     node_type = type(node).__name__
#     if node_type == 'Block':
#         return Block([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Assignment':
#         target = to_cfg(node.node)
#         value = to_cfg(node.expr)
#         if node.is_ref:
#             return RefAssign(target, value)
#         else:
#             return Assign(target, value)
#     elif node_type == 'ListAssignment':
#         targets = [to_cfg(n) for n in node.nodes]
#         value = to_cfg(node.expr)
#         return ListAssign(targets, value)
#     elif node_type == 'New':
#         args = [to_cfg(p) for p in node.params]
#         return New(node.name, args)
#     elif node_type == 'Clone':
#         return Clone(to_cfg(node.node))
#     elif node_type == 'Break':
#         return Break(to_cfg(node.node))
#     elif node_type == 'Continue':
#         return Continue(to_cfg(node.node))
#     elif node_type == 'Return':
#         return Return(to_cfg(node.node))
#     elif node_type == 'Yield':
#         return Yield(to_cfg(node.node))
#     elif node_type == 'Global':
#         return Global([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Static':
#         return Static([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Echo':
#         return Echo([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Print':
#         return Print(to_cfg(node.node))
#     elif node_type == 'Unset':
#         return Unset([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Try':
#         nodes = [to_cfg(n) for n in node.nodes]
#         catches = [to_cfg(c) for c in node.catches]
#         finally_ = to_cfg(node.finally_) if node.finally_ is not None else None
#         return Try(nodes, catches, finally_)
#     elif node_type == 'Catch':
#         class_ = node.class_
#         var = node.var
#         nodes = [to_cfg(n) for n in node.nodes]
#         return Catch(class_, var, nodes)
#     elif node_type == 'Finally':
#         return Finally([to_cfg(n) for n in node.nodes])
#     elif node_type == 'Throw':
#         return Throw(to_cfg(node.node))
#     elif node_type == 'Declare':
#         directives = [to_cfg(d) for d in node.directives]
#         node = to_cfg(node.node)
#         return Declare(directives, node)
#     elif node_type == 'Directive':
#         return Directive(node.name, to_cfg(node.node))
#     elif node_type == 'Function':
#         name = node.name
#         params = [to_cfg(p) for p in node.params]
#         nodes = [to_cfg(n) for n in node.nodes]
#         is_ref = node.is_ref
#         return Function(name, params, nodes, is_ref)
#     elif node_type == 'Method':
#         name = node.name
#         modifiers = node.modifiers
#         params = [to_cfg(p) for p in node.params]
#         nodes = [to_cfg(n) for n in node.nodes]
#         is_ref = node.is_ref
#         return Method(name, modifiers, params, nodes, is_ref)
#     elif node_type == 'Closure':
#         params = [to_cfg(p) for p in node.params]
#         vars = node.vars
#         nodes = [to_cfg(n) for n in node



# def ast_to_cfg(node):
#     if isinstance(node, ast.AST):
#         # 将节点类型转换为 CFG 中的基本块类型
#         if isinstance(node, ast.Module):
#             # 模块节点
#             return BasicBlock(node, None)
#         elif isinstance(node, ast.FunctionDef):
#             # 函数定义节点
#             return BasicBlock(node, None)
#         elif isinstance(node, ast.ClassDef):
#             # 类定义节点
#             return BasicBlock(node, None)
#         elif isinstance(node, ast.Expr):
#             # 表达式节点
#             return BasicBlock(node, None)
#         elif isinstance(node, ast.If):
#             # if 语句节点
#             return IfBlock(node)
#         elif isinstance(node, ast.While):
#             # while 语句节点
#             return WhileBlock(node)
#         elif isinstance(node, ast.For):
#             # for 语句节点
#             return ForBlock(node)
#         elif isinstance(node, ast.Assign):
#             # 赋值语句节点
#             return AssignBlock(node)
#         elif isinstance(node, ast.Return):
#             # 返回语句节点
#             return ReturnBlock(node)
#         elif isinstance(node, ast.Break):
#             # break 语句节点
#             return BreakBlock(node)
#         elif isinstance(node, ast.Continue):
#             # continue 语句节点
#             return ContinueBlock(node)
#         elif isinstance(node, ast.Try):
#             # try 语句节点
#             return TryBlock(node)
#         elif isinstance(node, ast.With):
#             # with 语句节点
#             return WithBlock(node)
#         elif isinstance(node, ast.Raise):
#             # raise 语句节点
#             return RaiseBlock(node)
#         elif isinstance(node, ast.Assert):
#             # assert 语句节点
#             return AssertBlock(node)
#         else:
#             raise TypeError(f"Unsupported node type: {type(node)}")
#     elif isinstance(node, list):
#         # 对于语句列表，将其转换为顺序执行的基本块列表
#         return [ast_to_cfg(child) for child in node]
#     else:
#         raise TypeError(f"Unsupported node type: {type(node)}")


# def build_cfg(node):
#     # 创建起始节点
#     start_block = BasicBlock(None, None)
#     # 将起始节点连接到程序入口节点
#     start_block.connect_to(ast_to_cfg(node))
#     #
#     if isinstance(node, ast.Assign):
#         assign_node = AssignNode(node.targets[0].id, build_expression(node.value))
#         return CFG(assign_node, assign_node)
#     elif isinstance(node, ast.While):
#         test_node = build_expression(node.test)
#         body_node = build_sequence(node.body)
#         while_node = WhileNode(test_node, body_node)
#         return CFG(while_node, while_node)

#     elif isinstance(node, ast.If):
#         test_node = build_expression(node.test)
#         body_node = build_sequence(node.body)
#         if_node = IfNode(test_node, body_node, None)
#         # 如果有else分支
#         if node.orelse:
#             else_node = build_sequence(node.orelse)
#             if_node.false_node = else_node
#             return CFG(if_node, body_node) + CFG(if_node, else_node)
#         else:
#             return CFG(if_node, body_node)

#     elif isinstance(node, ast.Return):
#         value_node = build_expression(node.value)
#         return_node = ReturnNode(value_node)
#         return CFG(return_node, return_node)

