import json
import os

file_path = 'data/likes/Npic.json'
file_dict = {}

try:
    with open(file_path, 'r') as f:
        file_dict = json.load(f)
except FileNotFoundError:
    pass

# 遍历目录下的文件名列表，将新文件名添加到字典中，并赋予空值
file_dir = 'static/Npic'
file_list = os.listdir(file_dir)
for file_name in file_list:
    if file_name not in file_dict:
        file_dict[file_name] = [0,0,0]

# 将更新后的字典序列化存储到文件中
with open(file_path, 'w') as f:
    json.dump(file_dict, f)



file_path = 'data/likes/pic.json'
file_dict = {}

try:
    with open(file_path, 'r') as f:
        file_dict = json.load(f)
except FileNotFoundError:
    pass

# 遍历目录下的文件名列表，将新文件名添加到字典中，并赋予空值
file_dir = 'static/pic'
file_list = os.listdir(file_dir)
for file_name in file_list:
    if file_name not in file_dict:
        file_dict[file_name] = [0,0,0]

# 将更新后的字典序列化存储到文件中
with open(file_path, 'w') as f:
    json.dump(file_dict, f)