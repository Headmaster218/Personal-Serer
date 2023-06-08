
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
pathes1 = os.listdir(file_dir+'国内')
pathes2 = os.listdir(file_dir+'欧美')
pathes3 = os.listdir(file_dir+'大哥')
keys = file_dict.keys()
new_file_dict = {}
for key, value in file_dict.items():
    if key in pathes1:
        new_file_dict['NSFW/国内/' + key] = value
    elif key in pathes2:
        new_file_dict['NSFW/欧美/' + key] = value
    elif key in pathes3:
        new_file_dict['NSFW/大哥/' + key] = value
    else:
        num+=1
# 将更新后的字典序列化存储到文件中
with open('data/likes/Npic.json', 'w') as f:
    json.dump(new_file_dict, f)
