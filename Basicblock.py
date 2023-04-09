from typing import List, Dict
from collections import defaultdict
from phply import phpast as php

import random

from TAC import TACInstruction


class BasicBlock:
    def __init__(self, name=None, instructions=None, predecessors=None, successors=None):
        self.name = name
        self.instructions = instructions if instructions is not None else []
        self.predecessors = predecessors if predecessors is not None else set()
        self.successors = successors if successors is not None else set()
        self.defs=set()
        self.uses=set()
        # 代表着之前的变量定义了，且之前的路径这个变量没有被重新定义
        self.Reach_IN=set() 
        # 代表了现在定义的变量在之后的路径可能会被使用，但是现在定义未被重新定义
        self.Reach_OUT=set()
        self.gen=set()
        self.kill=set()
        # IN集合包含所有在基本块入口之前被定义但在该基本块内被使用的变量
        self.Live_IN=set()
        # OUT集合包含所有在基本块内被定义但在该基本块出口之后被使用的变量
        self.Live_OUT=set()

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def add_predecessor(self, bb):
        self.predecessors.add(bb)

    def add_successor(self, bb):
        self.successors.add(bb)

    def __str__(self):
        return self.name

    def get_basic_block_by_name(self, name):
        for bb in self.basic_blocks:
            if bb.name == name:
                return bb
        return None



# def collect_basic_blocks(tac_instructions):
#     tac_instructions.insert(0,TACInstruction("LABEL",result="entry"))
#     basic_blocks = []  # 创建第一个基本块
#     flag=0 #判断是否需要新建bb  0：需要 1：no


#     for instruction in tac_instructions:
#         if flag==0 and instruction.op == "LABEL":
#             label = instruction.result
#             current_bb = BasicBlock(name=label)
#             continue


#         if    instruction.op == "IF":
#                 flag=0
#                 current_bb.add_instruction(instruction) #将当前保存
#                 basic_blocks.append(current_bb)
#                 next_bb=BasicBlock(name="next")
#                 current_bb=next_bb
#                 continue

#         if    instruction.op=="GOTO":
#                if current_bb.name=="next":
#                   current_bb.name==str(random.randint(100,1000))
#                   current_bb.add_instruction(instruction)
#                   flag=0
#                   basic_blocks.append(current_bb)
#                   next_bb=BasicBlock(name="next")
#                   current_bb=next_bb
#                   continue

#                else:
#                   flag=0
#                   current_bb.add_instruction(instruction)
#                   basic_blocks.append(current_bb)
#                   next_bb=BasicBlock(name="next")
#                   current_bb=next_bb
#                   continue


#         current_bb.add_instruction(instruction)
#         flag=1

#         if instruction.op=="LABEL":
#             current_bb.instructions.pop()
#             flag=0
#             basic_blocks.append(current_bb)
#             label = instruction.result
#             current_bb = BasicBlock(name=label)

#     return basic_blocks


# def collect_basic_blocks(tac_instructions):
#     tac_instructions.insert(0,TACInstruction("LABEL",result="entry"))
#     basic_blocks = []  # 创建第一个基本块
#     flag=0 #判断是否需要新建bb  0：需要 1：no


#     for instruction in tac_instructions:
#         if flag==0 and instruction.op == "LABEL":
#             label = instruction.result
#             current_bb = BasicBlock(name=label)
#             continue


#         if    instruction.op in ["IF","GOTO"]:
#                 flag=0
#                 current_bb.add_instruction(instruction) #将当前保存
#                 basic_blocks.append(current_bb)
#                 next_bb=BasicBlock(name="next")
#                 current_bb=next_bb
#                 continue

#         current_bb.add_instruction(instruction)
#         flag=1

#         if instruction.op=="LABEL":
#             current_bb.instructions.pop()
#             flag=0
#             basic_blocks.append(current_bb)
#             label = instruction.result
#             current_bb = BasicBlock(name=label)

#     return basic_blocks



def build_basic_blocks(tac_instructions):
    '''
    将tac收集成basicblocks
    '''

    tac_instructions.insert(0, TACInstruction("LABEL", result="entry"))
    basic_blocks = []  # 创建第一个基本块
    flag = 0  # 判断是否需要新建bb  0：需要 1：no

    for instruction in tac_instructions:
        if flag == 0 and instruction.op == "LABEL":
            label = instruction.result
            current_bb = BasicBlock(name=label)
            basic_blocks.append(current_bb)  # 将新创建的基本块添加到列表中
            continue

        if instruction.op in ["IF", "GOTO"]:
            flag = 0
            current_bb.add_instruction(instruction)  # 将当前保存
            next_bb = BasicBlock(name="next")
            current_bb = next_bb
            continue

        current_bb.add_instruction(instruction)
        flag = 1

        if instruction.op == "LABEL":
            current_bb.instructions.pop()
            flag = 0
            label = instruction.result
            current_bb = BasicBlock(name=label)
            basic_blocks.append(current_bb)  # 将新创建的基本块添加到列表中

    # if len(current_bb.instructions) > 0:
    #     basic_blocks.append(current_bb)

    return basic_blocks



def build_basic_block_edges(basic_blocks):
    for i, current_bb in enumerate(basic_blocks):
        # 如果当前基本块以 IF 或 GOTO 结束，那么将它们的目标作为后继
        if len(current_bb.instructions)==0:
            continue
        last_instruction = current_bb.instructions[-1]
        if last_instruction.op in ["GOTO","IF"]:
            target_label = last_instruction.jump_label

            # 寻找具有目标标签名称的基本块
            for target_bb in basic_blocks:
                if target_bb.name == target_label:
                    current_bb.add_successor(target_bb.name)
                    target_bb.add_predecessor(current_bb.name)
                    break

        # 如果当前指令为 IF 或 基本块的最后一条指令不是 GOTO，则将下一个基本块作为后继
        if i + 1 < len(basic_blocks) and  last_instruction.op != "GOTO":
            next_bb = basic_blocks[i + 1]
            current_bb.add_successor(next_bb.name)
            next_bb.add_predecessor(current_bb.name)



def print_basic_blocks(basic_blocks):
    for i, bb in enumerate(basic_blocks):
        print(f"Basic Block {i + 1}: {bb.name}")
        print("Predecessors:", [pred for pred in bb.predecessors])
        print("Successors:", [succ for succ in bb.successors])

        print("Instructions:")
        for inst in bb.instructions:
            print(f"  {inst}")

        print()



