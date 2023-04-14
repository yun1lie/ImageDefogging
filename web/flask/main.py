import os
import time

from FogRemover import FogRemover

import pymysql
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)

# 创建 MySQL 连接对象
db_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='image',
    autocommit=True,  # 自动提交事务
    charset='utf8mb4',  # 避免出现乱码
    cursorclass=pymysql.cursors.DictCursor,  # 指定返回结果为字典类型
)

# 配置 JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # 配置密钥
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # 配置 Token 过期时间
jwt = JWTManager(app)


# 自定义装饰器，用于验证用户 Token
@app.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    # 获取当前用户身份信息
    user_id = get_jwt_identity()

    # 在数据库中查询用户信息
    with db_conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE id=%s"
        cursor.execute(sql, user_id)
        result = cursor.fetchone()

        if not result:
            return jsonify(message='User not found'), 404

        # 移除密码字段，避免泄露敏感信息
        result.pop('password', None)

        return jsonify(user=result)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 在数据库中验证用户名和密码
    with db_conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': '用户名或密码错误'}), 401

        # 生成 Token 并返回给前端
        access_token = create_access_token(identity=result['id'])
        return jsonify({'token': access_token})


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    # 获取上传的文件
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'error': '未上传文件'}), 400

    # 保存文件，例如可以将文件名保存为当前时间戳
    save_path = f'static/{int(time.time())}.jpg'
    if not os.path.exists('static'):
        os.makedirs('static')
    uploaded_file.save(save_path)

    # 返回图片URL
    image_url = f'http://127.0.0.1:5000/{save_path}'
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'imageUrl': image_url
        }
    })


@app.route('/handleImage', methods=['POST'])
def handle_image():
    # 从请求中获取屏幕截图路径数据
    screen_image_url = request.json.get('screenImageUrl')
    url = './' + 'static' + screen_image_url.split('static')[1]
    # 进行处理操作
    # ...
    fr = FogRemover(url)
    fr.process()
    output_path = ''
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + \
        url.split(".")[1] + "_defog.jpg"

    return jsonify({'result': 'success', 'url': output_path})


if __name__ == '__main__':
    app.run(debug=True)
