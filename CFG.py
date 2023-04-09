from Basicblock import BasicBlock

class CFG:
    def __init__(self, basic_blocks):
        self.exit_bb = BasicBlock(name="exit")
        self.basic_blocks=basic_blocks

        # 将最后一个基本块连接到出口基本块
        self.exit_bb.add_predecessor(basic_blocks[-1].name)
        basic_blocks[-1].add_successor(self.exit_bb.name)
        self.basic_blocks = basic_blocks + [self.exit_bb]


    def add_basic_block(self, basic_block):
        self.basic_blocks.append(basic_block)

    def remove_basic_block(self, basic_block):
        self.basic_blocks.remove(basic_block)

    def get_basic_block_by_name(self, name):
        for bb in self.basic_blocks:
            if bb.name == name:
                return bb
        return None

    def __str__(self):
        result = "Control Flow Graph:\n"
        for bb in self.basic_blocks:
            result += f"  Basic Block {bb.name}:\n"
            result += f"    Predecessors: {[pred for pred in bb.predecessors]}\n"
            result += f"    Successors: {[succ for succ in bb.successors]}\n"
            for instruction in bb.instructions:
                result += f"      {instruction}\n"
        return result
