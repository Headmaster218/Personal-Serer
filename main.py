from flask import stream_with_context,send_from_directory,abort,Response,Flask, render_template, jsonify,request, redirect, url_for, session, send_file
from flask_session import Session
from werkzeug.utils import safe_join
from flask_sslify import SSLify
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
import os
import glob
import json
import random
import socket
from urllib.parse import unquote
import subprocess
import shlex
import word_sorter as ws

app = Flask(__name__)
# 强制使用 HTTPS
sslify = SSLify(app)
# 设置日志记录等级
app.logger.setLevel(logging.INFO)

# 创建日志记录处理器，用于写入日志文件（每 10k 循环一次）
handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=0)
handler.setLevel(logging.INFO)

# 定义日志记录格式
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

# 为应用添加日志记录处理器
app.logger.addHandler(handler)

app.config['STATIC_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['SECRET_KEY'] = 'asdb2[[/*$9)(/XSwncuwah#(&bcelu'  # Session 密钥
app.config['SESSION_TYPE'] = 'filesystem'  # Session 存储方式
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24 ) # Session 的有效期
Session(app)

with open('data/VIP_USERS.json', 'r') as f:
    file_data = f.read()
    VIP_USERS = json.loads(file_data)

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

Spic_urls = list(pic_imgs_dict.keys())
Npic_urls = list(Npic_imgs_dict.keys())

#爬虫
@app.route('/robots.txt', methods = ['GET'])
def anti_bot():
    return abort(403)

# 登录路由
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (username in VIP_USERS and VIP_USERS[username] == password) or (username in USERS and USERS[username] == password ):
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
    if session.get('username') in VIP_USERS or session.get('username') in USERS :
        return redirect(url_for('Home'))
    return render_template('login.html')

#注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        USERS[username] = password
        with open('data/USERS.json', 'w') as f:
            f.write(json.dumps(USERS))
        return jsonify({'success': 1})



# 图标路由
@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')

# 登出路由
@app.route('/logout')
def logout():
    # 删除 Session
    session.pop('username', None)
    return redirect(url_for('Home'))

# 主页路由
@app.route('/Home')
def Home():
    # 如果未登录，返回登录页
    if session.get('username') in VIP_USERS:
        username=1
    elif session.get('username') in USERS:
        username=2
    else:
        username=0
    return render_template('Home.html', username=username)

# 视频播放器路由
@app.route("/video", methods=['GET', 'POST'])
def video():
    if request.method == 'GET':
        video_urls = [r'static/example.mp4']
        if session.get('username') in VIP_USERS and session['username'] == 'Headmaster':
            with app.app_context():                
                for file_path in glob.glob(os.path.join('D:/HTML/Zzz/', '**/*.mp4'), recursive=True):
                    # 获取文件的相对路径（即从“Zzz”文件夹之后的部分）
                    relative_path = os.path.relpath(file_path, 'D:/HTML/Zzz/')
                    
                    # 创建视频的URL
                    video_url = url_for('static', filename=os.path.join('video', relative_path))
                    
                    # 将视频URL添加到列表中
                    video_urls.append(video_url)
                
        return render_template("video.html", video_urls=video_urls)
    # 预留上传视频功能
    elif request.method == 'POST':
        return render_template("video.html")

# 单独处理高级视频
@app.route('/static/video<string:subpath>')
def video_handler(subpath):
    if session.get('username') in VIP_USERS and session['username'] == 'Headmaster':

        decoded_url = unquote(subpath)
        path = r'D:\HTML\Zzz\\'+ decoded_url
        #return send_file(r'P:/《皇后乐队蒙特利尔现场演唱会》Queen.Rock.Montreal.And.Live.Aid.2007.720p.BluRay.x264-BDLiVE.mkv', as_attachment=False)
        #return send_file(r'P:/阿凡达2.mkv', as_attachment=False)
        return send_file(path, as_attachment=False)
    else:
        return render_template('login.html')

# 图片首页路由
@app.route("/pic", methods=['GET', 'POST'])
def pic():
    if request.method == 'GET':
        username = 0
        random.shuffle(Spic_urls)
        Npic_image_urls = Spic_urls
        if session.get('username') in VIP_USERS:
            username = 1
            random.shuffle(Npic_urls)
            Npic_image_urls = Npic_urls
        return render_template("pic.html", username=username, pic_image_urls=Spic_urls, Npic_image_urls=Npic_image_urls)
    #预留上传图片功能
    elif request.method == 'POST':
        return render_template("pic.html")

# 图片解析
@app.route('/pic_src/<path:subpath>')
def pic_handler(subpath):
    if subpath[:3] == "NSF":
        if session.get('username') in VIP_USERS:
            directory = r'D:/HTML'
            # 使用 safe_join 来确保路径安全
            path = safe_join(directory, subpath)
            # 检查路径是否在预期的目录中
            if path and os.path.exists(path):
                return send_file(path, as_attachment=True)
        else:
            return render_template('login.html')
    directory = r'D:/HTML'
    # 使用 safe_join 来确保路径安全
    path = safe_join(directory, subpath)
    # 检查路径是否在预期的目录中
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)

# 图片点赞路由
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

    if message[:3] == 'SFW':
        pic_dict_op_times+=1
        pic_imgs_dict[message][number] += 1
        return str(pic_imgs_dict[message][number])
    else:
        Npic_dict_op_times+=1
        Npic_imgs_dict[message][number] += 1
        return str(Npic_imgs_dict[message][number])

# 上传文件路由
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template("upload.html")
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Save uploaded file to disk
    file.save('D:/Programing/Code/个人服务器/upload/' + file.filename)
    return '上传成功'

# 背单词页面路由
@app.route("/word", methods=['GET'])
def word():
        return render_template("word.html")

#开始背单词
@app.route("/word/start", methods=['GET', 'POST'])
def word_start():
    user_name = session.get('username')
    if not user_name:
        return render_template('login.html')
    data = request.json
    text = data['text']
    base_path = os.path.join('.', 'data', 'user word', user_name)
    known_words_path = os.path.join(base_path, 'known_words.txt')
    unknown_words_path = os.path.join(base_path, 'unknown_words.txt')
    known_words = ws.load_word_set(known_words_path)
    unknown_words = ws.load_word_set(unknown_words_path)
    new_words = ws.process_text(text, known_words, unknown_words)
    if session.get('known_words_path') == None:
        session['known_words_path'] = known_words_path
    if session.get('unknown_words_path') == None:
        session['unknown_words_path'] = unknown_words_path

    return jsonify({'new_words': list(new_words)})

@app.route('/word/handle', methods=['POST'])
def handle_word():
    user_name = session.get('username')
    if not user_name:
        return jsonify({'error': 'User not logged in'}), 401
    data = request.json
    word = data.get('word')
    recognized = data.get('recognized')

    if recognized == 0:
        # 未识别
        ws.save_word(word, session.get('unknown_words_path'))
    elif recognized == 1:
        # 已识别
        ws.save_word(word, session.get('known_words_path'))
    elif recognized ==2:
        means = ws.extract_meaning_from_kmf(word)
        return jsonify({'success': 2, 'meaning': means})

    # 假设处理成功
    return jsonify({'success': 1})

# 托福文章路由
@app.route("/tofel/<path:subpath>", methods=['GET'])
def toefl(subpath):
    if subpath.startswith('reading'):
        # 获取 '/static/TOP reading' 目录下的所有文件名
        directory = os.path.join(app.static_folder, 'Tofel/reading')
        try:
            # 确保目录存在
            files = os.listdir(directory)
            # 返回文件名的列表
            return jsonify(files)
        except OSError as e:
            # 如果目录不存在或发生其他错误
            return jsonify({"error": str(e)}), 404
    elif subpath.startswith('listening'):
        # 获取 '/static/TOP listening' 目录下的所有文件名
        directory = os.path.join(app.static_folder, 'Tofel/listening')
        try:
            # 确保目录存在
            files = os.listdir(directory)
            # 返回文件名的列表
            return jsonify(files)
        except OSError as e:
            # 如果目录不存在或发生其他错误
            return jsonify({"error": str(e)}), 404
    elif subpath.startswith('article'):
        filename = subpath[8:]
        # 发送文件，假设文件存储在 'static/Tofel' 目录下
        return send_from_directory('static/Tofel', filename)
    


if __name__ == '__main__':
    context = ('data\pem\cert.pem', 'data\pem\key.pem')
    app.run(host=socket.getaddrinfo('wzh1615.top', None, socket.AF_INET6)[0][4][0], port=443, ssl_context=context)