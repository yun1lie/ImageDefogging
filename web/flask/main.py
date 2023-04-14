from flask import Flask, jsonify, request
import pymysql
from functools import wraps

import datetime
import jwt


app = Flask(__name__)


# 连接 MySQL 数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='image',
                             )


# 定义 get_user_from_database 函数
def get_user_from_database(token):
    # 创建一个游标对象
    with connection.cursor() as cursor:
        # 使用 SELECT 语句查询数据库中的用户信息
        sql = "SELECT * FROM users WHERE token=%s"
        cursor.execute(sql, (token,))
        result = cursor.fetchone()
        # 如果查询结果不为空，则返回用户信息的字典对象
        if result:
            return result
        else:
            return None

# 自定义装饰器，用于验证用户 Token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if verify_token(token):
            return f(*args, **kwargs)
        else:
            return jsonify(message='Authentication failed'), 401
    return decorated_function

# 验证用户 Token 的方法


def verify_token(token):
    # 进行 Token 的解密/验签等操作
    return True or False  # 根据实际情况返回 True 或 False


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    # username = request.form.get('username')
    # password = request.form.get('password')

    data = request.get_json()
    username = data['username']
    password = data['password']

    print(username, password)

    # 根据用户名和密码检查用户是否存在于数据库中
    user = check_user(username, password)

    if user:
        # 如果登录成功，返回 token 给前端
        token = generate_token(user)
        return jsonify({'token': token})
    else:
        # 如果登录失败，返回错误信息给前端
        return jsonify({'error': '用户名或密码错误'})


def check_user(username, password):
    # 在数据库中检查用户是否存在，并验证密码是否正确
    # 如果验证通过，返回用户对象；否则返回 None
    # 连接数据库
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='image',
                           )

    try:
        with conn.cursor() as cursor:
            # 查询用户名和密码是否匹配
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()

            if result:
                # 如果用户名和密码匹配，返回用户对象
                user = {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'phone': result[3],
                    'real_name': result[4],
                    'department': result[5],
                    'role': result[6]
                }
                return user
            else:
                # 如果用户名和密码不匹配，返回 None
                return None

    finally:
        # 关闭数据库连接
        conn.close()


def generate_token(user):
    # 根据用户信息生成 token，并存储在服务器端或发送给前端
    # 设置 token 过期时间为 1 小时
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # 生成 token
    token = jwt.encode(
        {'id': user['id'], 'exp': exp_time}, 'secret_key', algorithm='HS256')
    return token


# 用户信息接口
@app.route('/user', methods=['GET'])
@login_required
def get_user_info():
    # 从请求头中获取 Token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    # 进行 Token 的解密/验签等操作
    if verify_token(token):
        # 根据 Token 获取用户信息，并返回给前端
        user = get_user_from_database(token)
        return jsonify(user=user)
    else:
        # 如果 Token 验证失败，则返回 401 Unauthorized 状态码
        return jsonify(message='Authentication failed'), 401


# 关闭数据库连接
connection.close()


if __name__ == '__main__':
    app.run(debug=True)
