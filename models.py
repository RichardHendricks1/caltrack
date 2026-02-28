#!/usr/bin/env python3
"""
数据模型模块
"""

class Intake:
    """摄入记录模型"""
    def __init__(self, id, date, food, amount, calories, timestamp):
        self.id = id
        self.date = date
        self.food = food
        self.amount = amount
        self.calories = calories
        self.timestamp = timestamp

class Exercise:
    """运动记录模型"""
    def __init__(self, id, date, type, duration, calories, timestamp):
        self.id = id
        self.date = date
        self.type = type
        self.duration = duration
        self.calories = calories
        self.timestamp = timestamp

class DailySummary:
    """每日汇总模型"""
    def __init__(self, date, intake, burn, net):
        self.date = date
        self.intake = intake
        self.burn = burn
        self.net = net
