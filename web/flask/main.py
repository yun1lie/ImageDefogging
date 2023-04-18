from models import User, db
import os
import time
from datetime import datetime

from flask_bcrypt import Bcrypt


from FogRemover import FogRemover

import pymysql
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash
from flask_bcrypt import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/image'
db.init_app(app)
bcrypt = Bcrypt(app)

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
    # 从表单中获取数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 检查数据是否完整
    if not all(k in data for k in ("username", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    # 检查用户是否存在
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    print(password)
    print(user.password)
    print(check_password_hash(user.password, password))
    # 检查密码是否正确
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # 生成 JWT Token
    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=7))

    return jsonify({"access_token": access_token}), 200


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


@app.route('/register', methods=['POST'])
def register():
    # 从表单中获取数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    real_name = data.get('real_name')
    department = data.get('department')
    role = data.get('role')

    # 检查数据是否完整
    if not all(k in data for k in ("username", "password", "email")):
        return jsonify({"error": "Missing required fields"}), 400

    # 检查用户名是否已经被注册
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # 检查电子邮件是否已经被注册
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # 处理表单数据
    hashed_password = generate_password_hash(password).decode('utf-8')
    user = User(
        username=username,
        password=hashed_password,
        email=email,
        phone=phone,
        real_name=real_name,
        department=department,
        role=role,
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(user)
    db.session.commit()

    # 返回响应
    return jsonify({"message": "Register Success"}), 201


if __name__ == '__main__':
    app.run(debug=True)
