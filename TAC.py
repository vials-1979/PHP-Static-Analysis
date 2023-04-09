from phply import phpast as php

temp_variable_counter = 0

class TACInstruction:
    def __init__(self, op, left_operand=None, right_operand=None, result=None, jump_label=None):
        self.op = op
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
        self.jump_label = jump_label


    def __str__(self):
        if self.op == 'LABEL':
            return '{}:'.format(self.result)
        elif self.op == 'GOTO':
            return 'goto {}'.format(self.jump_label)
        elif self.op == 'IF':
            return 'if {} goto {}:'.format(self.left_operand, self.jump_label)
        elif self.op == 'PARAM':
            return 'param {}'.format(self.result)
        elif self.op == 'CALL':
            return '{} = call {}'.format(self.result, self.left_operand)
        elif self.op == 'RETURN':
            return 'return {}'.format(self.result)
        else:
            operands = []
            if self.result is not None:
                operands.append(str(self.result))
            if self.left_operand is not None:
                operands.append(str(self.left_operand))
            if self.right_operand is not None:
                operands.append(str(self.right_operand))

            return '{}  {} {}'.format(operands[0], self.op, ' '.join(operands[1:]))



def display_tac_instructions(tac_instructions):
    print("TAC Instructions:")
    for idx, instr in enumerate(tac_instructions, start=1):
        print(f"{idx}. {instr}")


def traverse_and_convert(node, tac_instructions,functions):
    '''
    遍历ast，对于ast结点进行tac转换，返回tac指令集合
    '''
    collect_functions(node,functions)

    if isinstance(node, list):
        for item in node:
            traverse_and_convert(item, tac_instructions,functions)
    elif isinstance(node, php.Node):
        if isinstance(node,php.Function):
            pass
        tac_instruction = create_tac_instruction(node,functions)
        if tac_instruction is not None:
            tac_instructions.extend(tac_instruction)



def collect_functions(node, functions):
    if isinstance(node, list):
        for item in node:
            collect_functions(item, functions)
    elif isinstance(node, php.Node):
        if isinstance(node, php.Function):
            function_name = node.name
            parameters = node.params

            # 处理函数体
            function_body = node.nodes
            function_tac_instructions = []

            for child in function_body:
                traverse_and_convert(child, function_tac_instructions,functions)

            #函数收集列表被更新
            functions[function_name] = {'function_tac_instructions': function_tac_instructions, 'parameters': parameters}





def create_tac_instruction(node,functions=None):
    '''
    生成tac指令集，对于传入的ast结点
    '''
    tac_instructions=[]


    if isinstance(node, php.Assignment):
        #除了assignment是op，其他都是result
        '''
        对赋值语句进行操作，主要对expr进行递归获得里面的指令集和，最后合并指令集
        其主要会影响赋值语句，函数调用，二元操作，一元操作，三元操作，数组等
        '''
        right_side = node.expr if isinstance(node.expr, (php.Variable, php.Constant, int, float, str)) else create_tac_instruction(node.expr)
        
        if not isinstance(right_side, (php.Variable, php.Constant, int, float, str)):
            tac_instructions.extend(right_side)
            right_side = right_side[-1].result

        tac_instructions.append(TACInstruction('=', left_operand=node.node.name,right_operand=right_side))

        return tac_instructions

    if isinstance(node, php.ListAssignment):
        return TACInstruction('list', [node.expr], node.nodes)

    if isinstance(node, php.Return):
       tac=process_expression(node.node)
       tac_instructions.extend(tac)
       temp_var=new_temporary_variable()
       TACInstruction('RETURN',result=temp_var)

       return tac_instructions

    if isinstance(node, php.Global):
        return TACInstruction('global', [node.nodes])

    if isinstance(node, php.Static):
        return TACInstruction('static', [node.nodes])

    if isinstance(node, php.Unset):
        return TACInstruction('unset', [node.nodes])

    if isinstance(node, php.AssignOp):
        '''
        对赋值类型作
        '''
        return [TACInstruction(node.op, node.left.name, node.right, result=node.left.name)]

    if isinstance(node, php.BinaryOp):
        left_operand = node.left if isinstance(node.left, (php.Variable, php.Constant, int, float,str)) else create_tac_instruction(node.left)
        right_operand = node.right if isinstance(node.right, (php.Variable, php.Constant, int, float,str)) else create_tac_instruction(node.right)

        if not isinstance(left_operand, (php.Variable, php.Constant, int, float,str)):
            tac_instructions.extend(left_operand)
            left_operand = left_operand[-1].result
        if not isinstance(right_operand, (php.Variable, php.Constant, int, float,str)):
            tac_instructions.extend(right_operand)
            right_operand = right_operand[-1].result

        temp_var = new_temporary_variable()
        tac_instructions.append(TACInstruction(node.op, left_operand, right_operand, temp_var))

        return tac_instructions
    

    if isinstance(node, php.UnaryOp):
        operand = node.expr if isinstance(node.expr, (php.Variable, php.Constant, int, float)) else create_tac_instruction(node.expr)
        
        if not isinstance(operand, (php.Variable, php.Constant, int, float)):
            tac_instructions.extend(operand)
            operand = operand[-1].result

        temp_var = new_temporary_variable()
        tac_instructions.append(TACInstruction(node.op, operand, None, temp_var))

        return tac_instructions



    if isinstance(node, php.TernaryOp):
        '''
        对于三元op，我们也是一样的操作，如果expr是常量，字符，非表达式直接就不处理了，如果不成立的话，我们就递归
        表达式求指令
        分支也可能有表达式：实际上表达式代表一切子节点
        对于三元表达式来说，正确分支与错误分支都要打上label，无论是错误分支与正确分支是什么类型，
        但是进入递归的时候我们无法控制label生成
        '''
        #条件指令集
        condition = process_expression(node.expr)
        tac_instructions.extend(condition)

        # Process the true branch and generate TAC instructions if needed
        #正确分支指令集
        true_branch = process_expression(node.iftrue)

        #错误分支指令集
        false_branch = process_expression(node.iffalse)

 
        true_label=new_temporary_variable()
        false_label=new_temporary_variable()
        end_label = new_temporary_variable()

        tac_instructions.append(TACInstruction("IF", condition[-1].result, None, jump_label=false_label))
        tac_instructions.append(TACInstruction("LABEL", None, None, true_label))
        tac_instructions.extend(true_branch)
        tac_instructions.append(TACInstruction("GOTO",None,None,jump_label=end_label))

        tac_instructions.append(TACInstruction("LABEL", None, None, false_label))
        tac_instructions.extend(false_branch) 
        
        tac_instructions.append(TACInstruction("LABEL", None, None, end_label))
        temp_var = new_temporary_variable()
        tac_instructions.append(TACInstruction("PHI", true_label, false_label, temp_var))

        return tac_instructions


    if isinstance(node, php.If):
        '''
        暂时打完收工
        '''
        # def process_branch(branch_node, next_label):
        #     if branch_node is not None:
        #         for child in  branch_node.nodes:
        #             tmp_tac=process_expression(child)
        #             tac_instructions.extend(tmp_tac)

        #     tac_instructions.append(TACInstruction("GOTO", None, None, next_label))
        
        condition = process_expression(node.expr)
        tac_instructions.extend(condition)


        true_label = new_temporary_variable()
        false_label = new_temporary_variable()
        end_label = new_temporary_variable()

        tac_instructions.append(TACInstruction("IF", condition[-1].result, None, jump_label=false_label))
        tac_instructions.append(TACInstruction("LABEL", None, None, true_label))
        process_branch(node.node, end_label,tac_instructions)

        for elseif in node.elseifs:
            tac_instructions.append(TACInstruction("LABEL", None, None, false_label))
            condition = process_expression(elseif.expr)
            tac_instructions.extend(condition)
            next_label = new_temporary_variable()

        # Add TAC instructions for the condition check and the jump to the next label
            tac_instructions.append(TACInstruction("IF", condition[-1].result, None, jump_label=next_label))

            process_branch(elseif.node, end_label,tac_instructions)

            false_label = next_label


        tac_instructions.append(TACInstruction("LABEL", None, None, false_label))
        process_branch(node.else_.node if node.else_ is not None else None, end_label,tac_instructions)

        # Add the end label
        tac_instructions.append(TACInstruction("LABEL", None, None, end_label))

        return tac_instructions
    

    if isinstance(node,php.Echo):
        '''
        测试版，暂时未完成
        '''
        if isinstance(node.nodes,list):
            temp_var=new_temporary_variable()
            tmp_instr=process_expression(node.nodes[0])
            tac_instructions.extend(tmp_instr)
            tac_instructions.append(TACInstruction(op="Echo",left_operand=tmp_instr[-1].result,result=temp_var))
            # return [TACInstruction(op="Echo",left_operand=tmp_instr[-1].result,result=temp_var)]
            return tac_instructions

    
    if isinstance(node,php.While):
        '''
        完工
        '''
        condition = process_expression(node.expr)
        body_tac = []

        for stmt in node.node.nodes:
            body_tac.extend(process_expression(stmt))

        loop_start_label = new_temporary_variable()
        tac_instructions.append(TACInstruction("LABEL", None, None, loop_start_label))
        tac_instructions.extend(condition)



        # 在循环条件为真时，跳转到循环体
        loop_body_label = new_temporary_variable()
        tac_instructions.append(TACInstruction("IF", condition[-1].result, None, jump_label=loop_body_label))

        # 在循环条件为假时，跳出循环
        loop_end_label = new_temporary_variable()
        next_label=new_temporary_variable()
        tac_instructions.append(TACInstruction("LABEL", None, None, next_label))
        tac_instructions.append(TACInstruction("GOTO", None, None, jump_label=loop_end_label))

        # 循环体
        tac_instructions.append(TACInstruction("LABEL", None, None, loop_body_label))
        tac_instructions.extend(body_tac)

        # 循环结束后，跳回循环开始，再次检查循环条件
        tac_instructions.append(TACInstruction("GOTO", None, None, jump_label=loop_start_label))

        # 循环结束标签
        tac_instructions.append(TACInstruction("LABEL", None, None, loop_end_label))

        return tac_instructions



    if isinstance(node, php.PreIncDecOp):
        return TACInstruction(node.op, [node.expr])

    if isinstance(node, php.PostIncDecOp):
        return TACInstruction(node.op, [node.expr])

    if isinstance(node, php.Cast):
        return TACInstruction('cast', [node.type, node.expr])

    if isinstance(node, php.IsSet):
        return TACInstruction('isset', [node.nodes])

    if isinstance(node, php.Empty):
        return TACInstruction('empty', [node.expr])

    if isinstance(node, php.Eval):
        #result
        params = []

        params=process_expression(node.expr)

        tac_instructions.extend(params)
        tac_instructions.append(TACInstruction("PARAM",result=params[-1].result))
        # 创建一个新的临时变量用于存储函数调用结果
        temp_var = new_temporary_variable()
        tac_instructions.append(TACInstruction("CALL", 'eval', None,temp_var))

        return  tac_instructions



    if isinstance(node, php.Include):
        return TACInstruction('include_once' if node.once else 'include', [node.expr])

    if isinstance(node, php.Require):
        return TACInstruction('require_once' if node.once else 'require', [node.expr])
    
    if isinstance(node, php.Exit):
        return TACInstruction('exit' if node.type == 0 else 'die', [node.expr])

    if isinstance(node, php.Silence):
        return TACInstruction('silence', [node.expr])

    if isinstance(node, php.StaticVariable):
        return TACInstruction('static_variable', [node.name, node.initial])
    
    if isinstance(node, php.LexicalVariable):
        return TACInstruction('lexical_variable', [node.name, node.is_ref])

    if isinstance(node, php.FormalParameter):
        return TACInstruction('formal_parameter', [node.name, node.default, node.is_ref, node.type])
    

    if isinstance(node, php.FunctionCall):
        '''
        也许还有缺陷，返回调用结果是result
        '''
        params = []
        tmp_params=[]

        for param in node.params:
            params.extend(process_expression(param.node))



        for p in params:
            tac_instructions.append(p)
            tac_instructions.append(TACInstruction("PARAM",result=p.result))
            tmp_params.append(p.result)

        # 创建一个新的临时变量用于存储函数调用结果
        temp_var = new_temporary_variable()

        # 生成函数调用TAC指令
        func_name = node.name

        #函数参数是右值
        tac_instructions.append(TACInstruction("CALL", func_name,right_operand=tmp_params,result=temp_var))

        return  tac_instructions


    if isinstance(node, php.Array):
        return TACInstruction('array', [create_tac_instruction(n) for n in node.nodes])

    if isinstance(node, php.ArrayElement):
        return TACInstruction('array_element', [create_tac_instruction(node.key), create_tac_instruction(node.value), node.is_ref])


    if isinstance(node, php.ArrayOffset):
        #全局变量获取，op=LOAD_ARRAY_OFFSET
        temp_var=new_temporary_variable()
        # 添加LOAD_ARRAY_OFFSET指令
        # print(node.node.name)
        # print(node.expr)
        tac_instructions.append(TACInstruction("LOAD_ARRAY_OFFSET", node.node.name, node.expr,result=temp_var))
        return tac_instructions



    if isinstance(node, php.StringOffset):
        return TACInstruction('string_offset', [create_tac_instruction(node.node), create_tac_instruction(node.expr)])

    if isinstance(node, php.ObjectProperty):
        return TACInstruction('object_property', [create_tac_instruction(node.node), node.name])

    if isinstance(node, php.StaticProperty):
        return TACInstruction('static_property', [create_tac_instruction(node.node), node.name])

    if isinstance(node, php.MethodCall):
        return TACInstruction('method_call', [create_tac_instruction(node.node), node.name, [create_tac_instruction(n) for n in node.params]])

    if isinstance(node, php.StaticMethodCall):
        return TACInstruction('static_method_call', [node.class_, node.name, [create_tac_instruction(n) for n in node.params]])



def process_expression(expr):
    '''
    返回子节点指令集
    '''
    tmp_instr=[]
    if isinstance(expr, (php.Variable, php.Constant, int, float, str)):
        temp_var = new_temporary_variable()
        tmp_instr.append(TACInstruction("LOAD", expr, None, temp_var))
        return tmp_instr
    else:
        expr_instructions = create_tac_instruction(expr)
        tmp_instr.extend(expr_instructions)
        return tmp_instr


def new_temporary_variable():
    global temp_variable_counter
    temp_variable_name = 't{}'.format(temp_variable_counter)
    temp_variable_counter += 1
    return temp_variable_name



def get_branches(node):
    """
    Given an AST node, return a list of all its branches.
    """
    branches = []

    # If the node is an If statement, add its branches
    if isinstance(node, php.If):
        branches.append(node.node.nodes)
        for elseif in node.elseifs:
            branches.append(elseif.node.nodes)
        if node.else_ is not None:
            branches.append(node.else_.node.nodes)

    # If the node is a While or Do-While loop, add its branch
    elif isinstance(node, (php.While, php.DoWhile)):
        branches.append(node.node.nodes)

    # If the node is a For or Foreach loop, add its branch
    elif isinstance(node, (php.For, php.Foreach)):
        branches.append(node.node.nodes)

    # If the node is a Switch statement, add its branches
    elif isinstance(node, php.Switch):
        for case in node.nodes:
            branches.append(case.nodes)

    return branches


def process_branch(branch_node, next_label,tac_instructions):
    if branch_node is not None:
        for child in  branch_node.nodes:
            tmp_tac=process_expression(child)
            tac_instructions.extend(tmp_tac)

    # tmp_var=new_temporary_variable()

    # tac_instructions.append(TACInstruction("LABEL", None, None, result=tmp_var))
    tac_instructions.append(TACInstruction("GOTO", None, None, jump_label=next_label))