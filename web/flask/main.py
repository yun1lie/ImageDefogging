from datetime import datetime, timedelta
import os
import time
import cv2

import pymysql
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

from FogRemover import FogRemover
from models import User, db

from DCP import Dehaze
from Clahe import Clahe
from cap import Cap

from NonLocalDehazer import NonLocalDehazer

import retinex

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/image'
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 避免出现警告
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='image',
    autocommit=True,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)

# 处理静态文件请求


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    with db_conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE id=%s"
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
        if not result:
            return jsonify(message='User not found'), 404
        result.pop('password', None)
        return jsonify(user=result)


@app.route('/getUser', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    # 根据用户id查询用户信息
    cursor = db_conn.cursor()
    sql = "select * from users where id=%s"
    cursor.execute(sql, (user_id))
    user_info = cursor.fetchall()
    print(user_info)
    # 将用户信息转换为JSON格式并返回
    return jsonify(user_info)

# 处理查询用户信息的请求


@app.route('/users', methods=['GET'])
def get_users():

    # 查询用户信息的SQL语句
    query_users_sql = "SELECT * FROM users"
    # 创建游标对象
    cursor = db_conn.cursor()
    # 执行查询用户信息的SQL语句
    cursor.execute(query_users_sql)
    # 获取查询结果
    rows = cursor.fetchall()
    # 关闭游标和数据库连接
    cursor.close()
    # 返回查询结果
    return jsonify({'users': rows})

# 处理删除用户信息的请求


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # 删除用户信息的SQL语句
    delete_user_sql = "DELETE FROM users WHERE id=%s"
    print(delete_user_sql)

    # 创建游标对象
    cursor = db_conn.cursor()
    # 执行删除用户信息的SQL语句
    cursor.execute(delete_user_sql, (user_id,))
    # 提交事务
    db_conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    # 返回删除成功的信息
    return jsonify({'message': 'User deleted successfully'})


# 管理员修改用户个人信息
@app.route('/userInfo/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    # 创建游标对象
    # cursor = db_conn.cursor()
    # sql = "UPDATE `image`.`users` SET `username` = 'admin32', `email` = 'admin3@example.com2', `phone` = '123456789082', `real_name` = '管理员三2', `department` = '系统管理部门2', `role` = '系统管理员2' WHERE `id` = 8"
    with db_conn.cursor() as cursor:
        # 更新用户信息
        # 执行更新操作
        sql = 'UPDATE users SET  department=%s, email=%s, phone=%s, real_name=%s, role=%s, username=%s WHERE id=%s'
        print(sql)
        cursor.execute(sql, (data.get('department'), data.get('email'), data.get(
            'phone'), data.get('real_name'), data.get('role'), data.get('username'), user_id))

        db_conn.commit()
        return jsonify(data)

    print(data)
    return None


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not all(k in data for k in ("username", "password")):
        return jsonify({"error": "Missing required fields"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=7))
    return jsonify({"token": access_token}), 200


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'error': '未上传文件'}), 400
    save_path = f'static/{int(time.time())}.jpg'
    if not os.path.exists('static'):
        os.makedirs('static')
    uploaded_file.save(save_path)
    image_url = f'http://127.0.0.1:5000/{save_path}'
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'imageUrl': image_url}})


@app.route('/handleImage', methods=['POST'])
def handle_image():
    screen_image_url = request.json.get('screenImageUrl')
    url = './' + 'static' + screen_image_url.split('static')[1]
    img = cv2.imread(url)

    config = [15, 80, 250]
    img_amsrcr = retinex.automatedMSRCR(
        img,
        config
    )
    output_path = '.' + \
        url.split(".")[0] + \
        url.split(".")[1] + "_defog.jpg"
    cv2.imwrite(output_path, img_amsrcr)
    # fr = FogRemover(url)
    # fr.process()
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_defog.jpg"
    increase_retinex_count()  # 数据库中使用数量加1
    return jsonify({'result': 'success', 'url': output_path})


@app.route('/handleDCP', methods=['POST'])
def hadnle_image_DCP():
    screen_image_url = request.json.get('screenImageUrl')
    min_filter_radius = request.json.get('min_filter_radius')
    guided_filter_radius = request.json.get('guided_filter_radius')
    guided_filter_epsilon = request.json.get('guided_filter_epsilon')
    v1_limit = request.json.get('v1_limit')
    v1_weight = request.json.get('v1_weight')
    bins = request.json.get('bins')
    gamma_correction_enabled = request.json.get('gamma_correction_enabled')
    print(min_filter_radius)
    url = './' + 'static' + screen_image_url.split('static')[1]
    dcp = Dehaze(min_filter_radius, guided_filter_radius,
                 guided_filter_epsilon, v1_limit, v1_weight, bins, gamma_correction_enabled)
    print(dcp.min_filter_radius, url)
    dcp.process_images(url)
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_defogDCP.jpg"
    increase_dcp_count()
    return jsonify({'result': 'success', 'url': output_path})


@app.route('/handleLocal', methods=['POST'])
def hadnle_image_Local():
    screen_image_url = request.json.get('screenImageUrl')
    url = './' + 'static' + screen_image_url.split('static')[1]
    nld = NonLocalDehazer(url)
    nld.run()
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_NonLocal.jpg"
    increase_NonLocal_count()
    return jsonify({'result': 'success', 'url': output_path})


@app.route('/handleClahe', methods=['POST'])
def hadnle_image_Clahe():
    screen_image_url = request.json.get('screenImageUrl')
    url = './' + 'static' + screen_image_url.split('static')[1]

    clahe = Clahe(url)
    clahe.split_channels()
    clahe.apply_clahe()
    clahe.merge_channels()

    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_CLAHE.jpg"
    clahe.save_images()
    increase_CLAHE_count()
    return jsonify({'result': 'success', 'url': output_path})


@app.route('/handleCap', methods=['POST'])
def hadnle_image_Cap():
    screen_image_url = request.json.get('screenImageUrl')
    url = './' + 'static' + screen_image_url.split('static')[1]
    dehaze = Cap(url, beta=1)
    dehaze.dehaze()
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_Cap.jpg"
        
    increase_CAP_count()

    return jsonify({'result': 'success', 'url': output_path})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not all(k in data for k in ("username", "password", "email")):
        return jsonify({"error": "Missing required fields"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    hashed_password = generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password, email=email, phone=data.get('phone'), real_name=data.get(
        'real_name'), department=data.get('department'), role=data.get('role'), create_time=datetime.now(), update_time=datetime.now())
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Register Success"}), 201


@app.route('/userMan', methods=['POST'])
def userMan():
    data = request.get_json()
    user_id = data.get('id')
    department = data.get('department')
    with db_conn.cursor() as cursor:
        # 更新用户信息
        # 执行更新操作
        sql = 'UPDATE users SET  department=%s, email=%s, phone=%s, real_name=%s, role=%s, username=%s WHERE id=%s'
        print(sql)
        cursor.execute(sql, (data.get('department'), data.get('email'), data.get(
            'phone'), data.get('real_name'), data.get('role'), data.get('username'), user_id))

        db_conn.commit()
        return jsonify(db_conn.commit())
    return data


# 获取算法统计信息
@app.route("/algorithm-usage")
def get_algorithm_usage():
    algorithm_usage = {
        "retinexCount": 0,
        "dcpCount": 0,
        "NonLocalCount": 0,
        "capCount": 0,
        "CLAHECount": 0,

    }
    with db_conn.cursor() as cursor:
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name=%s"
        cursor.execute(sql, ('retinex',))
        result = cursor.fetchone()
        if result:
            algorithm_usage['retinexCount'] = result['usage_count']

        cursor.execute(sql, ('dcp',))
        result = cursor.fetchone()
        if result:
            algorithm_usage['dcpCount'] = result['usage_count']
            
        
        cursor.execute(sql, ('NonLocal',))
        result = cursor.fetchone()
        if result:
            algorithm_usage['NonLocalCount'] = result['usage_count']
            
        
        cursor.execute(sql, ('CLAHE',))
        result = cursor.fetchone()
        if result:
            algorithm_usage['CLAHECount'] = result['usage_count']
            
        cursor.execute(sql, ('CAP',))
        result = cursor.fetchone()
        if result:
            algorithm_usage['capCount'] = result['usage_count']

    return jsonify(algorithm_usage)

# 增加retinex函数


def increase_retinex_count():
    with db_conn.cursor() as cursor:
        # 查询当前使用次数
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name='retinex'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            usage_count = result['usage_count'] + 1
            # 更新使用次数
            sql = "UPDATE algorithm_usage SET usage_count=%s WHERE algorithm_name='retinex'"
            cursor.execute(sql, (usage_count,))
        else:
            # 如果不存在记录，插入新的记录
            sql = "INSERT INTO algorithm_usage (algorithm_name, usage_count) VALUES (%s, %s)"
            cursor.execute(sql, ('retinex', 1))
    db_conn.commit()


def increase_dcp_count():
    with db_conn.cursor() as cursor:
        # 查询当前使用次数
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name='dcp'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            usage_count = result['usage_count'] + 1
            # 更新使用次数
            sql = "UPDATE algorithm_usage SET usage_count=%s WHERE algorithm_name='dcp'"
            cursor.execute(sql, (usage_count,))
        else:
            # 如果不存在记录，插入新的记录
            sql = "INSERT INTO algorithm_usage (algorithm_name, usage_count) VALUES (%s, %s)"
            cursor.execute(sql, ('dcp', 1))
    db_conn.commit()
    
def increase_NonLocal_count():
    with db_conn.cursor() as cursor:
        # 查询当前使用次数
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name='NonLocal'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            usage_count = result['usage_count'] + 1
            # 更新使用次数
            sql = "UPDATE algorithm_usage SET usage_count=%s WHERE algorithm_name='NonLocal'"
            cursor.execute(sql, (usage_count,))
        else:
            # 如果不存在记录，插入新的记录
            sql = "INSERT INTO algorithm_usage (algorithm_name, usage_count) VALUES (%s, %s)"
            cursor.execute(sql, ('NonLocal', 1))
    db_conn.commit()
    
def increase_CLAHE_count():
    with db_conn.cursor() as cursor:
        # 查询当前使用次数
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name='CLAHE'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            usage_count = result['usage_count'] + 1
            # 更新使用次数
            sql = "UPDATE algorithm_usage SET usage_count=%s WHERE algorithm_name='CLAHE'"
            cursor.execute(sql, (usage_count,))
        else:
            # 如果不存在记录，插入新的记录
            sql = "INSERT INTO algorithm_usage (algorithm_name, usage_count) VALUES (%s, %s)"
            cursor.execute(sql, ('CLAHE', 1))
    db_conn.commit()
    

def increase_CAP_count():
    with db_conn.cursor() as cursor:
        # 查询当前使用次数
        sql = "SELECT * FROM algorithm_usage WHERE algorithm_name='CAP'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            usage_count = result['usage_count'] + 1
            # 更新使用次数
            sql = "UPDATE algorithm_usage SET usage_count=%s WHERE algorithm_name='CAP'"
            print(sql)
            cursor.execute(sql, (usage_count,))
        else:
            # 如果不存在记录，插入新的记录
            sql = "INSERT INTO algorithm_usage (algorithm_name, usage_count) VALUES (%s, %s)"
            cursor.execute(sql, ('CAP', 1))
    db_conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
