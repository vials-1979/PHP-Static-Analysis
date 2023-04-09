import os
import re
import codecs

from pprint import pprint


from phply.phplex import lexer  # 词法分析
from phply.phpparse import make_parser  # 语法分析
from phply import phpast as php
from typing import List, Dict
from collections import defaultdict
from graphviz import Digraph

import graphviz

from live_value import compute_defs_uses,live_dataflow_analysis

from TaintAnalysis import TaintAnalysis
from rules.BaseVulnerabilityRule import VulnerabilitySet,CommandExecutionVulnerability


from reach_variable import compute_gen_kill,reach_dataflow_analysis

from Basicblock import BasicBlock, build_basic_blocks,print_basic_blocks,build_basic_block_edges


from CFG import CFG

import yaml

from TAC import (
    traverse_and_convert,
    create_tac_instruction,
    display_tac_instructions,
    get_branches,
)


def create_digraph_from_bb_list(bb_list):
    # 创建一个有向图
    digraph = Digraph()

    # 遍历基本块列表，将基本块添加到有向图中
    for bb in bb_list:
        digraph.node(bb.label)

        # 遍历每个基本块的后继，并在有向图中添加边
        for succ in bb.successors:
            digraph.edge(bb.label, succ.label)

    return digraph



def parser_code(path):
    all_nodes = []
    filepath = r"C:\Users\vials\Desktop\毕业设计\MyPHPScan\tests\{}".format(path)

    fi = codecs.open(filepath, "r", encoding="utf-8", errors="ignore")
    code_content = fi.read()
    fi.close()
    parser = make_parser()
    all_nodes = parser.parse(code_content, debug=False, lexer=lexer.clone(), tracking=True)


    tacs = []
    functions = {}
    traverse_and_convert(all_nodes, tacs, functions)



    bbs=[]
    bbs=build_basic_blocks(tacs)

    build_basic_block_edges(bbs)

    print(bbs)

    live_dataflow_analysis(bbs,compute_defs_uses)

    reach_dataflow_analysis(bbs)

    cfg=CFG(bbs)


    CE=CommandExecutionVulnerability()
    taint=TaintAnalysis(cfg,CE)

    func=taint.find_dangerous_function_calls()

    # print(func)

    paths=taint.find_taint_paths()


    res=taint.analyze(paths)
    for i in res:
        i['file']=path
    
    return res

# if __name__ == '__main__':
#     parser_code('CE.php')
    




# for i in bbs:
#     # if i.name=='t2':
#         # print(i.Reach_IN)
#         # # print(i.gen)
#         # # print(i.kill)
#         # print(i.Reach_OUT)

#         # print(i.uses)

#         # print(i.defs)

#         print("------------")




# print_basic_blocks(bbs)


# print(cfg)

# with open("cfg.txt", "wt") as f:
#     print(cfg, file=f)




# for tets in tacs:
#     print(tets)




# with open("res.txt", "w") as f:
#     for i in tacs:
#         f.write(i.__str__()+"\n")


# for i in a:
#     print(i)


# dot = '''
# digraph ControlFlowGraph {
#     label="Control Flow Graph";
#     node [shape=rectangle];

#     entry0 [label="Basic Block entry:\nPredecessors: []\nSuccessors: ['entry']"];
#     entry1 [label="Basic Block entry:\nPredecessors: ['entry']\nSuccessors: ['t14']\n$a = 1\n$b = 2\n$c = 0\nt4 = $a + $b\n$c = t4"];
#     t14 [label="Basic Block t14:\nPredecessors: ['entry', 't10']\nSuccessors: ['t15', 't17']\nt5 = $a < 10\nif t5 goto t15"];
#     t17 [label="Basic Block t17:\nPredecessors: ['t14']\nSuccessors: ['t16']\ngoto t16"];
#     t15 [label="Basic Block t15:\nPredecessors: ['t14']\nSuccessors: ['t8', 't9']\nt6 = $a + $b\n$c = t6\nt7 = $c > 5\nif t7 goto t9"];
#     t8 [label="Basic Block t8:\nPredecessors: ['t15']\nSuccessors: ['t10']\nparam t11 = LOAD $a\nparam t12 = LOAD $b\nt13 = call foo\n$d = t13\nEcho = 'Result: ' . $d . '\\n'\ngoto t10"];
#     t9 [label="Basic Block t9:\nPredecessors: ['t15']\nSuccessors: ['t10']\ngoto t10"];
#     t10 [label="Basic Block t10:\nPredecessors: ['t8', 't9']\nSuccessors: ['t14']\n$a += $a 1\ngoto t14"];
#     t16 [label="Basic Block t16:\nPredecessors: ['t17']\nSuccessors: ['exit']"];
#     exit0 [label="Basic Block exit:\nPredecessors: ['t16']\nSuccessors: []"];

#     entry0 -> entry1;
#     entry1 -> t14;
#     t14 -> t15;
#     t14 -> t17;
#     t17 -> t16;
#     t15 -> t8;
#     t15 -> t9;
#     t8 -> t10;
#     t9 -> t10;
#     t10 -> t14;
#     t16 -> exit0;
# }

# '''

# graph = graphviz.Source(dot)
# graph.render(filename='example', format='png')


#     print(i.jump_label)

# display_tac_instructions(tacs)


# print(all_nodes[0].expr)

# for i in all_nodes:
#    print(create_tac_instruction(i))

# bb_list=[]

# process_ast_nodes(all_nodes,bb_list,0,None,False)
# show_predecessors_successors_content(bb_list)


# digraph = create_digraph_from_bb_list(bb_list)
# digraph.view()
