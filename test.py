import os
import re
import string 
import numpy as np

# from CFG import CFG


# file_path='C:/Users/vials\Desktop\毕业设计\MyPHPScan\a.php'
# with open(file_path, 'r') as f:
#     content = f.read()
#     class_names = re.findall(r'\bclass\b\s+\b[A-Z]\w*\b', content)
#     # type(class_names)
    
#     class_names.append(file_path)

#     print(class_names)

# # 正则获取类名，文件位置，第几行

# a=CFG(100)

# print(a.test)

a={'x',0,'a','c','i'}
a=set(a)

for i in range(len(a)):
    print(a.pop())