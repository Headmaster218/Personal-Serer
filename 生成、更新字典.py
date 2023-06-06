import json
import os

def update_file_dict(file_dirs, file_dict):
    num = 0
    for file_dir in file_dirs:
        file_list = os.listdir(file_dir)
        for file_name in file_list:
            if file_name not in file_dict:
                file_dict[file_name] = [0, 0, 0]
                num += 1
    return num

file_dict = {}
try:
    with open('data/likes/Npic.json', 'r') as f:
        file_dict = json.load(f)
except FileNotFoundError:
    pass
num=0
# 遍历目录下的文件名列表，将新文件名添加到字典中，并赋予空值
file_dir = 'D:/HTML/NSFW/'
num += update_file_dict(['D:/HTML/NSFW/国内', 'D:/HTML/NSFW/欧美', 'D:/HTML/NSFW/大哥'], file_dict)
print(num)
# 将更新后的字典序列化存储到文件中
with open('data/likes/Npic.json', 'w') as f:
    json.dump(file_dict, f)


file_dict = {}
try:
    with open('data/likes/pic.json', 'r') as f:
        file_dict = json.load(f)
except FileNotFoundError:
    pass
num=0
# 遍历目录下的文件名列表，将新文件名添加到字典中，并赋予空值
num += update_file_dict(['D:/HTML/SFW/国内', 'D:/HTML/SFW/欧美', 'D:/HTML/SFW/大哥'], file_dict)
print(num)
# 将更新后的字典序列化存储到文件中
with open('data/likes/pic.json', 'w') as f:
    json.dump(file_dict, f)