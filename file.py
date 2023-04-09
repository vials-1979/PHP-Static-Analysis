import re
import os
import string
import codecs

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


ignore_ext_list=['html','gif','png','jpg']

check_ext_list=['php','inc']

Class_info=[]



path=r"C:\Users\vials\Desktop\seacmsv10_jb51\SeaCMS12.9\Upload\admin"

for root,dirs,files in os.walk(path):
    for file in files:
        if file.endswith("php") or file.endswith("inc"):
            file_path=os.path.join(root,file)
            # print(os.path.join(root,file))

            file = codecs.open(file_path, "r", encoding='utf-8', errors='ignore')
            content = file.read()
            class_names = re.findall(r'\bclass\b\s+\b[A-Z]\w*\b', content)

            class_names.append(file_path)

            Class_info.append(class_names)

        #   简单的获取到了类的信息与所处文件  ['C:\\Users\\vials\\Desktop\\seacmsv10_jb51\\SeaCMS12.9\\Upload\\admin\\admin_ads.php']







            
            # 获取每一个类的信息