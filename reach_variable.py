import Basicblock
from phply import phpast as php


def compute_gen_kill(basic_blocks):
    """
    Compute the gen and kill sets for each basic block
    """
    # Step 1: Collect all variable definitions from all basic blocks
    var_defs = set()
    for block in basic_blocks:
        for instr in block.instructions:
            if instr.op in ['=', '+=', '-=', '*=', '/=', '|=', '&=']:
                var_defs.add(instr.left_operand)
    
    # Step 2: Compute gen and kill sets for each basic block
    for block in basic_blocks:
        block.gen = set()
        block.kill = set()
        for instr in block.instructions:
            if instr.op in ['=', '+=', '-=', '*=', '/=', '|=', '&=']:
                var_def = instr.left_operand
                if var_def in var_defs:
                    # The variable definition is new and belongs to gen set
                    block.gen.add(var_def)
                    var_defs.remove(var_def)
                else:
                    # The variable definition is old and belongs to kill set
                    block.kill.add(var_def)


def reach_dataflow_analysis(basic_blocks):
    '''
    有修改，现在不清楚修改会导致什么后果
    '''
    """
    Computes the IN and OUT sets for each basic block using the worklist algorithm for the
    reachability dataflow analysis.
    """
    # Step 1: Compute the gen and kill sets for each basic block
    compute_gen_kill(basic_blocks)

    # Step 2: Initialize OUT sets for each basic block
    for block in basic_blocks:
        block.Reach_OUT = set()

    # Step 3: Create the worklist with all basic blocks
    worklist = set(basic_blocks)

    # Step 4: Iterate until the worklist is empty
    while worklist:
        # Step 4.1: Pick a basic block B from Worklist.
        B = worklist.pop()

        if isinstance(B,str):
            for bb in basic_blocks:
                if bb.name== B:
                    B=bb

        # Step 4.2: Compute the new IN set.
        temp=B.Reach_OUT

        new_IN = set()
        for P in B.predecessors:
           if isinstance(P,str):
                for bb in basic_blocks:
                    if bb.name== P:
                        P=bb
           new_IN.update(P.Reach_OUT)
           
        B.Reach_IN=new_IN

        # Step 4.3: Compute the new OUT set.
        B.Reach_OUT = B.gen.union(new_IN - B.kill)


        # Step 4.4: Check if OUT set has changed.
        if temp != B.Reach_OUT:
            # B.Reach_OUT = new_OUT

            # # Step 4.5: Add all successors of B to Worklist.
            worklist.update(B.successors)
