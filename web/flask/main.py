from flask import Flask, jsonify, request
import pymysql

import datetime
import jwt


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
