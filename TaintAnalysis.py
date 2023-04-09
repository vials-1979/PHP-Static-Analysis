from rules.SourceRule import SourceRule
# from rules.BaseVulnerabilityRule import  CommandExecutionVulnerability
from phply import phpast as php




class TaintAnalysis:
    def __init__(self, cfg, vulnerability_rules):
        self.cfg = cfg
        self.vulnerability_rules = vulnerability_rules

    def is_vulnerable(self, node, function_name):
        if function_name in self.vulnerability_rules.sensitive_sinks:  
            if not self.is_filtered(node):
                return True
        return False

    def is_filtered(self, node):
        for filter_function in self.vulnerability_rules.filter_functions:
            if filter_function in node:  # 检查过滤函数是否在节点中
                return True
        return False

   
    def get_function_call_parameters(self, tac_instructions, start_index):
        parameters = []

        #start_index就是函数调用位置即CALL指令的位置,暂时不考虑传入参数可能是变量表达式和变量操作的情况下，我们现在只考虑参入参数为变量和常数
        if start_index is not None:
            for i in tac_instructions[start_index].right_operand:
                for j in range(start_index-1,-1,-1):
                    if tac_instructions[j].result==i and tac_instructions[j].op!='PARAM':
                        if isinstance(tac_instructions[j].left_operand,php.Variable):
                            parameters.append(tac_instructions[j].left_operand.name)
                            break
                        else:
                            parameters.append(tac_instructions[j].left_operand)
                            break


        return parameters





    def find_dangerous_function_calls(self):
        dangerous_function_calls = []

        for node in self.cfg.basic_blocks:

            for i, statement in enumerate(node.instructions):
                if self.is_function_call(statement):
                    function_name = self.get_function_name(statement)
                    if self.is_dangerous_function(function_name):
                        #获取参数
                        parameters=self.get_function_call_parameters(node.instructions,i)
                        dangerous_function_calls.append({"node": node.name, "function": function_name,"parameters":parameters})

        return dangerous_function_calls




    
    def is_dangerous_function(self, function_name):
        return function_name in self.vulnerability_rules.sensitive_sinks


    
    def is_variable_reachable(self, variable, reach_in, gen, kill):
        if variable in reach_in:
            return True
        elif variable in gen:
            return True
        elif variable in kill:
            return False
        else:
            # 需要进一步检查前驱基本块来确定变量的可达性
            return None


    def find_taint_paths(self):
        dangerous_function_calls = self.find_dangerous_function_calls()
        taint_paths = []

        for call in dangerous_function_calls:
            bb_name = call["node"]
            bb = self.cfg.get_basic_block_by_name(bb_name)
            reach_in = bb.Reach_IN
            gen=bb.gen
            kill=bb.kill

            #获取参数并判断是否可达，若是可达则污点分析的有效路径从此开始，反向寻找敏感宿及可能存在的过滤函数
            for parameter in call["parameters"]:
                if self.is_variable_reachable(parameter, reach_in,gen,kill):
                    ##bb：当前有sink函数调用的basicblock
                    taint_path = self.backward_taint_analysis(bb, parameter) 
                
                    # Check for security filter functions along the taint path
                    path_is_tainted = True
                    for block in taint_path:
                        if self.has_security_filter_function(block):
                            path_is_tainted = False
                            break

                    if path_is_tainted:
                        singgle_path=[]
                        for tmp in taint_path:
                            singgle_path.append(tmp.name)
                            
                        taint_paths.append({
                            "sink": call["function"],
                            "parameter": parameter,
                            "path": singgle_path
                        })

        #             taint_path = {
        #                 "source": parameter,
        #                 "sink": call["function"],
        #                 "node": bb_name
        #             }
        #             taint_paths.append(taint_path)

        return taint_paths


    def backward_taint_analysis(self, starting_block, parameter):
        taint_path = []
        visited_blocks = set()

        def visit_block(block):
            if block.name in visited_blocks:
                return

            visited_blocks.add(block.name)
            taint_path.append(block)

            # Find predecessors with the parameter in their Reach_OUT set
            for pred in block.predecessors:
                if isinstance(pred,str):
                    pred= self.cfg.get_basic_block_by_name(pred)


                if self.is_variable_reachable(parameter, pred.Reach_OUT, pred.gen, pred.kill):
                    visit_block(pred)

        visit_block(starting_block)
        return taint_path



    def has_security_filter_function(self, block):
        for statement in block.instructions:
            if self.is_function_call(statement):
                function_name = self.get_function_name(statement)
                if self.is_security_filter_function(function_name):
                    return True
        return False

    def is_security_filter_function(self,function_name):
        if function_name in  self.vulnerability_rules.filter_functions:
            return True
        
        return False

    def analyze(self, taint_path):
        vulnerabilities = []
        for single_taint_path in taint_path:
            if single_taint_path['sink'] in self.vulnerability_rules.sensitive_sinks:
                # # 遍历每个漏洞规则
                # for vulnerability_rule in self.vulnerability_rules.vulnerabilities:
                #     # 检查当前污点路径是否与漏洞规则匹配
                #     if vulnerability_rule.is_match(single_taint_path):
                        # 如果匹配，打印检测到的漏洞信息
                        # print(f"Detected vulnerability: CommandExecutionVulnerability")
                        # print(f"Sink: {single_taint_path['sink']}")
                        # print(f"Parameter: {single_taint_path['parameter']}")
                        # print(f"Path: {single_taint_path['path']}")
                        # print("------")
                    vulnerability = {
                        'type': 'CommandExecutionVulnerability',
                        'sink': single_taint_path['sink'],
                        'parameter': single_taint_path['parameter'],
                        'path': single_taint_path['path']
                    }
                    vulnerabilities.append(vulnerability)
        
        return vulnerabilities

        

        

    def is_function_call(self, statement):
        if statement.op=="CALL":
            return True
        
        return False

    def get_function_name(self, statement):
        # 在此实现从语句中获取函数名称的逻辑
        return  statement.left_operand