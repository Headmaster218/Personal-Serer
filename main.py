from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_session import Session
from flask_sslify import SSLify
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

# 创建日志记录处理器，用于写入日志文件（每 10k 循环一次）
handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=10)
handler.setLevel(logging.INFO)

# 定义日志记录格式
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

# 为应用添加日志记录处理器
app.logger.addHandler(handler)

app.config['STATIC_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['SECRET_KEY'] = 'asdb2[[/*$9)(/XSwncuwah#(&bcelu'  # Session 密钥
app.config['SESSION_TYPE'] = 'filesystem'  # Session 存储方式
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Session 的有效期
Session(app)

with open('data/USERS.json', 'r') as f:
    file_data = f.read()
    USERS = json.loads(file_data)

# 图片点赞信息存储在字典中[喜，踩，错]
with open('data/likes/Npic.json', 'r') as f:   # 打开一个JSON数据文件
    file_data = f.read()                     # 读取文件内容
    Npic_imgs_dict = json.loads(file_data)   # 将JSON格式数据解析为Python对象

with open('data/likes/pic.json', 'r') as f:   # 打开一个JSON数据文件
    file_data = f.read()                     # 读取文件内容
    pic_imgs_dict = json.loads(file_data)   # 将JSON格式数据解析为Python对象
pic_dict_op_times = 0
Npic_dict_op_times = 0

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username] == password:
            if(session.get('wrong_times') == None or session['wrong_times'] < 10):
                # 验证通过，创建 Session
                session['username'] = username
                app.logger.info(username+'登录成功')
                return redirect(url_for('Home'))
        else:
            # 验证失败
            session.setdefault('wrong_times', 0)  # 使用setdefault函数初始化错误次数为0
            session['wrong_times'] += 1
            app.logger.warning(f"{request.remote_addr} 用户名或密码错误 {username} {password}")
            error_msg = f"用户名或密码错误，已尝试{session['wrong_times']}次"
            if session['wrong_times'] > 5:
                error_msg += f"\n行为已记录，您的ip: {request.remote_addr}"
            session['IP'] = request.remote_addr  # 不管验证是否成功，都应该记录用户IP
            return render_template('login.html', error_msg=error_msg)
    # elif request.method==('GET'):
    # 如果已登录，直接跳转到主页
    if session.get('username') in USERS:
        return redirect(url_for('Home'))
    return render_template('login.html')

@app.route('/Home')
def Home():
    # 如果未登录，返回登录页
    if session.get('username') in USERS:
        username=1
    else:
        username=0
    return render_template('Home.html', username=username)

# 图片路由
@app.route("/pic", methods=['GET', 'POST'])
def pic():
    if request.method == 'GET':
        pic_image_urls = []
        Npic_image_urls = []
        username = 0
        for file_path in glob.glob(os.path.join(app.config['STATIC_FOLDER'], 'pic', '*.jpg')):
            img_url = url_for('static', filename='pic/' + os.path.basename(file_path))
            pic_image_urls.append(img_url)
            random.shuffle(pic_image_urls)
        if session.get('username') in USERS:
            with app.app_context():
                username = 1
                for file_path in glob.glob(os.path.join(app.config['STATIC_FOLDER'], 'Npic', '*.jpg')):
                    img_url = url_for('static', filename='Npic/' + os.path.basename(file_path))
                    Npic_image_urls.append(img_url)
                    random.shuffle(Npic_image_urls)
        return render_template("pic.html", username=username, pic_image_urls=pic_image_urls, Npic_image_urls=Npic_image_urls)
    #预留上传图片功能
    elif request.method == 'POST':
        return render_template("pic.html")

# 单独处理高级图片
@app.route('/static/Npic/<string:subpath>')
def path_handler(subpath):
    if session.get('username') in USERS:
        return send_file(r'D:\Programing\Code\个人服务器\static\Npic\\'+subpath)
    else:
        return render_template('login.html')


# 点赞路由
@app.route("/like", methods=['POST'])
def like():
    global pic_dict_op_times, Npic_dict_op_times
    number = int(request.form.get("btn"))  # 获取数字类型数据
    message = request.form.get("path")  # 获取字符串类型数据
    if(pic_dict_op_times%5==0):
        with open('data/likes/Npic.json', 'w') as f:
            json.dump(Npic_imgs_dict, f)
    if(Npic_dict_op_times%5==0):
        with open('data/likes/pic.json', 'w') as f:
            json.dump(pic_imgs_dict, f)

    if message[:11] == '/static/pic':
        pic_dict_op_times+=1
        pic_imgs_dict[message[12:]][number] += 1
        return str(pic_imgs_dict[message[12:]][number])
    else:
        Npic_dict_op_times+=1
        Npic_imgs_dict[message[13:]][number] += 1
        return str(Npic_imgs_dict[message[13:]][number])


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