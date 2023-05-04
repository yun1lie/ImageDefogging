from datetime import datetime, timedelta
import os
import time

import pymysql
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

from FogRemover import FogRemover
from models import User, db

from DCP import Dehaze

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
    fr = FogRemover(url)
    fr.process()
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_defog.jpg"
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
    print(dcp.min_filter_radius,url)
    dcp.process_images(url)
    output_path = 'http://127.0.0.1:5000/' + \
        url.split(".")[0] + url.split(".")[1] + "_defogDCP.jpg"
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


if __name__ == '__main__':
    app.run(debug=True)
