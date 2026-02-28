#!/usr/bin/env python3
"""
CalTrack 本地服务器
数据存储在本地 data.json 文件
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域访问

DATA_FILE = 'data.json'

def get_data():
    """读取数据"""
    if not os.path.exists(DATA_FILE):
        return {'intake': [], 'exercise': []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_records():
    """获取所有记录"""
    data = get_data()
    return jsonify(data)

@app.route('/api/intake', methods=['POST'])
def add_intake():
    """添加食物摄入"""
    req = request.json
    data = get_data()

    record = {
        'id': int(datetime.now().timestamp() * 1000),
        'date': req['date'],
        'name': req['name'],
        'amount': req['amount'],
        'calories': req['calories'],
        'time': req['time']
    }

    data['intake'].append(record)
    save_data(data)

    return jsonify({'success': True, 'record': record})

@app.route('/api/exercise', methods=['POST'])
def add_exercise():
    """添加运动消耗"""
    req = request.json
    data = get_data()

    record = {
        'id': int(datetime.now().timestamp() * 1000),
        'date': req['date'],
        'type': req['type'],
        'duration': req['duration'],
        'calories': req['calories'],
        'time': req['time']
    }

    data['exercise'].append(record)
    save_data(data)

    return jsonify({'success': True, 'record': record})

@app.route('/api/<record_type>/<int:record_id>', methods=['DELETE'])
def delete_record(record_type, record_id):
    """删除记录"""
    if record_type not in ['intake', 'exercise']:
        return jsonify({'error': 'Invalid type'}), 400

    data = get_data()
    data[record_type] = [r for r in data[record_type] if r['id'] != record_id]
    save_data(data)

    return jsonify({'success': True})

if __name__ == '__main__':
    print('\n🚀 CalTrack 服务器启动中...')
    print('📱 在手机浏览器中访问: http://<你的电脑IP>:3000')
    print('🖥️  在电脑浏览器中访问: http://localhost:3000')
    print('📂 数据文件:', os.path.abspath(DATA_FILE))
    print('⏹️  按 Ctrl+C 停止服务器\n')

    app.run(host='0.0.0.0', port=3000, debug=False)
