#!/usr/bin/env python3
"""
CalTrack 本地服务器
数据存储在 Obsidian Vault 中
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import fcntl
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Obsidian Vault 路径（iCloud Drive）
VAULT_PATH = '/Users/starktony/Library/Mobile Documents/iCloud~md~obsidian/Documents/SillyIsSmart'
DATA_FILE = os.path.join(VAULT_PATH, 'CalTrack 记录.md')
JSON_DATA_FILE = os.path.join(VAULT_PATH, '.caltrack_data.json')

def ensure_vault_exists():
    """确保 vault 存在"""
    if not os.path.exists(VAULT_PATH):
        print(f"❌ Obsidian Vault 不存在: {VAULT_PATH}")
        return False
    return True

def get_data():
    """从 JSON 文件读取数据"""
    if not os.path.exists(JSON_DATA_FILE):
        return {'intake': [], 'exercise': []}

    with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data_to_json(data):
    """保存数据到 JSON 文件（带文件锁）"""
    with open(JSON_DATA_FILE, 'w', encoding='utf-8') as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # 获取排他锁
        json.dump(data, f, ensure_ascii=False, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)  # 释放锁

def generate_markdown():
    """生成 Markdown 文件"""
    data = get_data()

    # 按 ID 排序（倒序，新的在前）
    intake = sorted(data['intake'], key=lambda x: x['id'], reverse=True)
    exercise = sorted(data['exercise'], key=lambda x: x['id'], reverse=True)

    today = datetime.now().strftime('%Y-%m-%d')
    today_intake = sum(r['calories'] for r in intake if r['date'] == today)
    today_burn = sum(r['calories'] for r in exercise if r['date'] == today)

    content = f"""---
tag: caltrack
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
---

# CalTrack - 卡路里追踪

> 数据由 CalTrack 服务器自动生成和更新

## 今日统计 ({today})

| 摄入 | 消耗 | 净摄入 |
|------|------|--------|
| {today_intake} | {today_burn} | {today_intake - today_burn} |

## 摄入记录

| ID | 日期 | 名称 | 数量 | 卡路里 | 时间 |
|----|------|------|------|--------|------|
"""

    for r in intake:
        content += f"| `{r['id']}` | {r['date']} | {r['name']} | {r['amount']} | {r['calories']} | {r['time']} |\n"

    content += "\n## 运动记录\n\n| ID | 日期 | 类型 | 时长 | 卡路里 | 时间 |\n|----|------|------|------|--------|------|\n"

    for r in exercise:
        content += f"| `{r['id']}` | {r['date']} | {r['type']} | {r['duration']}分钟 | {r['calories']} | {r['time']} |\n"

    return content

def update_markdown():
    """更新 Markdown 文件"""
    content = generate_markdown()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

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
    save_data_to_json(data)
    update_markdown()

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
    save_data_to_json(data)
    update_markdown()

    return jsonify({'success': True, 'record': record})

@app.route('/api/<record_type>/<int:record_id>', methods=['DELETE'])
def delete_record(record_type, record_id):
    """删除记录"""
    if record_type not in ['intake', 'exercise']:
        return jsonify({'error': 'Invalid type'}), 400

    data = get_data()
    data[record_type] = [r for r in data[record_type] if r['id'] != record_id]
    save_data_to_json(data)
    update_markdown()

    return jsonify({'success': True})

if __name__ == '__main__':
    if not ensure_vault_exists():
        exit(1)

    # 初始化 Markdown 文件
    update_markdown()

    print('\n🚀 CalTrack 服务器启动中...')
    print('📱 在手机浏览器中访问: http://<你的电脑IP>:9000')
    print('🖥️  在电脑浏览器中访问: http://localhost:9000')
    print(f'📂 Obsidian Vault: {VAULT_PATH}')
    print(f'📄 数据文件: {DATA_FILE}')
    print(f'📦 JSON 备份: {JSON_DATA_FILE}')
    print('⏹️  按 Ctrl+C 停止服务器\n')

    app.run(host='0.0.0.0', port=9000, debug=False)
