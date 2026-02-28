#!/usr/bin/env python3
"""
命令模块
"""

from datetime import datetime

def add_food(db, food, amount, calories):
    """添加食物摄入"""
    db.add_intake(food, amount, calories)
    print(f"✓ 已记录: {food} {amount} - {calories} kcal")

def add_exercise(db, exercise_type, duration, calories):
    """添加运动记录"""
    db.add_exercise(exercise_type, duration, calories)
    print(f"✓ 已记录: {exercise_type} {duration}分钟 - {calories} kcal")

def show_today(db, summary_only=False):
    """显示今日记录"""
    today = datetime.now().strftime('%Y-%m-%d')
    summary = db.get_daily_summary(today)

    if summary_only:
        print(f"\n📅 {today} 汇总")
        print(f"  摄入: {summary['intake']} kcal")
        print(f"  消耗: {summary['burn']} kcal")
        print(f"  净摄入: {summary['net']} kcal")
        return

    intake = db.get_today_intake()
    exercise = db.get_today_exercise()

    print(f"\n📅 {today}")
    print("\n🍽️ 摄入:")
    if intake:
        for record in intake:
            print(f"  {record[3]} {record[4]} - {record[5]} kcal")
    else:
        print("  (无记录)")

    print("\n🏃 运动:")
    if exercise:
        for record in exercise:
            print(f"  {record[3]} {record[4]}分钟 - {record[5]} kcal")
    else:
        print("  (无记录)")

    print(f"\n📊 汇总: 摄入 {summary['intake']} kcal | 消耗 {summary['burn']} kcal | 净 {summary['net']} kcal")

def show_history(db, days=7):
    """显示历史记录"""
    history = db.get_history(days)

    if not history:
        print("\n📜 暂无历史记录")
        return

    print(f"\n📜 最近 {len(history)} 天记录:")
    print("-" * 50)
    for record in history:
        print(f"{record['date']}: 摄入 {record['intake']} | 消耗 {record['burn']} | 净 {record['net']} kcal")

def show_summary(db, date=None):
    """显示指定日期汇总"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    summary = db.get_daily_summary(date)

    print(f"\n📅 {date} 汇总")
    print(f"  摄入: {summary['intake']} kcal")
    print(f"  消耗: {summary['burn']} kcal")
    print(f"  净摄入: {summary['net']} kcal")

def show_stats(db):
    """显示统计信息"""
    stats = db.get_stats()

    print("\n📊 统计信息")
    print("-" * 30)
    print(f"  总摄入: {stats['total_intake']} kcal")
    print(f"  总消耗: {stats['total_burn']} kcal")
    print(f"  净摄入: {stats['net']} kcal")
    print(f"  记录天数: 摄入 {stats['intake_days']} 天 | 运动 {stats['exercise_days']} 天")
