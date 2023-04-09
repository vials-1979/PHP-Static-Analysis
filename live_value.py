import Basicblock
from phply import phpast as php

class Lattice:
    """
    Lattice for active variable analysis
    """

    def __init__(self, in_set, out_set):
        self.in_set = set(in_set)
        self.out_set = set(out_set)

    def __eq__(self, other):
        return self.in_set == other.in_set and self.out_set == other.out_set

    def __lt__(self, other):
        return self.in_set.issubset(other.in_set) and self.out_set.issuperset(other.out_set)

    def __le__(self, other):
        return self.in_set.issubset(other.in_set) and self.out_set.issuperset(other.out_set)

    def __gt__(self, other):
        return self.in_set.issuperset(other.in_set) and self.out_set.issubset(other.out_set)

    def __ge__(self, other):
        return self.in_set.issuperset(other.in_set) and self.out_set.issubset(other.out_set)

    def __hash__(self):
        return hash((frozenset(self.in_set), frozenset(self.out_set)))

    def __str__(self):
        return f'({self.in_set}, {self.out_set})'


def compute_defs_uses(basic_blocks):
    """
    Compute variable definitions and uses for each basic block
    """
    for block in basic_blocks:
        block.defs = set()
        block.uses = set()
        for instr in block.instructions:
            if instr.op in ["=", "-=","+=","/=","%=","*=","&=","|="]:
                block.defs.add(instr.left_operand)
            elif isinstance(instr.left_operand,php.Variable) or isinstance(instr.right_operand,php.Variable):
                if isinstance(instr.left_operand,php.Variable):
                    block.uses.add(instr.left_operand.name)
                
                elif  isinstance(instr.right_operand,php.Variable):
                    block.uses.add(instr.right_operand.name)

                else:
                    block.uses.add(instr.left_operand.name)
                    block.uses.add(instr.right_operand.name)

     

def live_dataflow_analysis(basic_blocks, compute_defs_uses):
    # Compute defs and uses for each basic block
    compute_defs_uses(basic_blocks)

    # Initialize IN and OUT sets for each basic block
    for block in basic_blocks:
        block.Live_IN = set()
        block.Live_OUT = set()

    # Create the worklist with all basic blocks
    worklist = basic_blocks.copy()

    while worklist:
        # Pop a basic block from the worklist
        B = worklist.pop()

        if isinstance(B,str):
            for bb in basic_blocks:
                if bb.name== B:
                    B=bb

        # Compute the new OUT set
        if not B.successors:
            new_out = set()
        else:
            successors = [bb for bb in basic_blocks if bb.name in B.successors]
            new_out = set.intersection(*(S.Live_IN for S in successors))

        # Compute the new IN set
        if not B.predecessors:
            new_in=set()
        else:
            new_in = B.uses.union(new_out - B.defs)

        # Check if IN or OUT sets have changed
        if new_in != B.Live_IN or new_out != B.Live_OUT:
            B.Live_IN, B.Live_OUT = new_in, new_out

            # Add predecessors to the worklist
            worklist.extend(B.predecessors)
