#!/usr/bin/env python3
"""
工具函数模块
"""

from datetime import datetime

def get_today_date():
    """获取今日日期字符串"""
    return datetime.now().strftime('%Y-%m-%d')

def format_datetime(dt):
    """格式化日期时间"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def format_date(dt):
    """格式化日期"""
    return dt.strftime('%Y-%m-%d')

def parse_date(date_str):
    """解析日期字符串"""
    return datetime.strptime(date_str, '%Y-%m-%d')
