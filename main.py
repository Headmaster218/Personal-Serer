from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sslify import SSLify
import bcrypt
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
import os
import glob
import json
import random

app = Flask(__name__)
# 强制使用 HTTPS
sslify = SSLify(app)
# 设置日志记录等级
app.logger.setLevel(logging.INFO)

# 创建日志记录处理器，用于写入日志文件（每 1M 循环一次）
handler = RotatingFileHandler('flask.log', maxBytes=1000000, backupCount=10)
handler.setLevel(logging.INFO)

# 定义日志记录格式
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

# 为应用添加日志记录处理器
app.logger.addHandler(handler)

app.config['STATIC_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['SECRET_KEY'] = 'asdb2[[/*$9)(/XSwncuwah#(&bcelu'  # Session 密钥
app.config['SESSION_TYPE'] = 'filesystem'  # Session 存储方式
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) # Session 的有效期
Session(app)

# 用户信息存储在字典中
USERS = {
    'Headmaster': 'Wzh021013',
    '20205482': '123qwe',
    '20205329': 'g1234567',
    'wjl_father': 'wjlismyson'
}
salt = bcrypt.gensalt()
i=0
hashed_username = [None] * len(USERS)
for key in USERS:
    hashed_username[i] = bcrypt.hashpw(key.encode(), salt).decode()
    i+=1

# 图片点赞信息存储在字典中[喜，踩，错]
with open('data/likes/NSFW.json', 'r') as f:   # 打开一个JSON数据文件
    file_data = f.read()                     # 读取文件内容
    NSFW_imgs_dict = json.loads(file_data)   # 将JSON格式数据解析为Python对象

with open('data/likes/SFW.json', 'r') as f:   # 打开一个JSON数据文件
    file_data = f.read()                     # 读取文件内容
    SFW_imgs_dict = json.loads(file_data)   # 将JSON格式数据解析为Python对象


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username] == password:
            # 验证通过，创建 Session
            session['username'] = bcrypt.hashpw(username.encode(), salt).decode()
            return redirect(url_for('Home'))
        else:
            # 验证失败，回到登录页并显示错误消息
            error_msg = '用户名或密码错误'
            return render_template('login.html', error_msg=error_msg)

    # 如果已登录，直接跳转到主页
    if session.get('username')  in hashed_username:
        return redirect(url_for('Home'))

    return render_template('login.html')

@app.route('/Home')
def Home():
    # 如果未登录，返回登录页
    if session.get('username') in hashed_username:
        username=1
    else:
        username=0
    return render_template('Home.html', username=username)

# 图片路由
@app.route("/pic", methods=['GET', 'POST'])
def pic():
    if request.method == 'GET':
        SFW_image_urls = []
        NSFW_image_urls = []
        username = 0
        for file_path in glob.glob(os.path.join(app.config['STATIC_FOLDER'], 'SFW', '*.jpg')):
            img_url = url_for('static', filename='SFW/' + os.path.basename(file_path))
            SFW_image_urls.append(img_url)
            random.shuffle(SFW_image_urls)
        if session.get('username') in hashed_username:
            with app.app_context():
                username = 1
                for file_path in glob.glob(os.path.join(app.config['STATIC_FOLDER'], 'NSFW', '*.jpg')):
                    img_url = url_for('static', filename='NSFW/' + os.path.basename(file_path))
                    NSFW_image_urls.append(img_url)
                    random.shuffle(NSFW_image_urls)
        return render_template("pic.html", username=username, SFW_image_urls=SFW_image_urls, NSFW_image_urls=NSFW_image_urls)
    elif request.method == 'POST':
        button = request.form['button']
        pic_path = request.form['pic_path']
        return render_template("pic.html")

# 点赞路由
@app.route("/like", methods=['POST'])
def like():
    number = int(request.form.get("btn"))  # 获取数字类型数据
    message = request.form.get("path")  # 获取字符串类型数据
    if message[:11] == '/static/SFW':
        SFW_imgs_dict[message[12:]][number] += 1
        print(SFW_imgs_dict[message[12:]][number])
    else:
        NSFW_imgs_dict[message[13:]][number] += 1
    return '1'

# 上传文件路由
@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route('/upload-file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Save uploaded file to disk
    file.save('D:/Programing/Code/个人服务器/upload/' + file.filename)
    return '上传成功'


if __name__ == '__main__':
    context = ('.\cert.pem', '.\key.pem')
    app.run(host='172.20.35.15', port=443, ssl_context=context)