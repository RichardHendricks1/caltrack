#!/usr/bin/env python3
"""
数据库操作模块
"""

import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='caltrack.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化数据库，创建表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建摄入记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                food TEXT NOT NULL,
                amount TEXT NOT NULL,
                calories INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        # 创建运动记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                duration INTEGER NOT NULL,
                calories INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    def add_intake(self, food, amount, calories, date=None):
        """添加摄入记录"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO intake (date, food, amount, calories, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, food, amount, calories, timestamp))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def add_exercise(self, exercise_type, duration, calories, date=None):
        """添加运动记录"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO exercise (date, type, duration, calories, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, exercise_type, duration, calories, timestamp))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_today_intake(self, date=None):
        """获取今日摄入记录"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM intake WHERE date = ? ORDER BY timestamp DESC
        ''', (date,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_today_exercise(self, date=None):
        """获取今日运动记录"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM exercise WHERE date = ? ORDER BY timestamp DESC
        ''', (date,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_daily_summary(self, date=None):
        """获取每日汇总"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        conn = self.get_connection()
        cursor = conn.cursor()

        # 摄入总卡路里
        cursor.execute('SELECT SUM(calories) FROM intake WHERE date = ?', (date,))
        total_intake = cursor.fetchone()[0] or 0

        # 运动总卡路里
        cursor.execute('SELECT SUM(calories) FROM exercise WHERE date = ?', (date,))
        total_burn = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'date': date,
            'intake': total_intake,
            'burn': total_burn,
            'net': total_intake - total_burn
        }

    def get_history(self, days=7):
        """获取历史记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        dates = []
        for i in range(days):
            date = datetime.now().strftime('%Y-%m-%d')
            dates.append(date)

        history = []
        for date in dates:
            summary = self.get_daily_summary(date)
            if summary['intake'] > 0 or summary['burn'] > 0:
                history.append(summary)

        conn.close()
        return history

    def get_stats(self):
        """获取统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 总摄入
        cursor.execute('SELECT SUM(calories) FROM intake')
        total_intake = cursor.fetchone()[0] or 0

        # 总运动
        cursor.execute('SELECT SUM(calories) FROM exercise')
        total_burn = cursor.fetchone()[0] or 0

        # 记录天数
        cursor.execute('SELECT COUNT(DISTINCT date) FROM intake')
        intake_days = cursor.fetchone()[0] or 0

        cursor.execute('SELECT COUNT(DISTINCT date) FROM exercise')
        exercise_days = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_intake': total_intake,
            'total_burn': total_burn,
            'net': total_intake - total_burn,
            'intake_days': intake_days,
            'exercise_days': exercise_days
        }
