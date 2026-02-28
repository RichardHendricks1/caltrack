#!/usr/bin/env python3
"""
CalTrack - 卡路里追踪工具
命令行工具，用于记录每日卡路里摄入和运动消耗
"""

import argparse
from datetime import datetime
from db import Database
from commands import add_food, add_exercise, show_today, show_history, show_summary, show_stats

def main():
    parser = argparse.ArgumentParser(description='CalTrack - 卡路里追踪工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # add-food 子命令
    food_parser = subparsers.add_parser('add-food', help='添加食物摄入记录')
    food_parser.add_argument('food', help='食物名称')
    food_parser.add_argument('amount', help='数量')
    food_parser.add_argument('--calories', '-c', type=int, required=True, help='卡路里')

    # add-exercise 子命令
    exercise_parser = subparsers.add_parser('add-exercise', help='添加运动消耗记录')
    exercise_parser.add_argument('type', help='运动类型')
    exercise_parser.add_argument('duration', type=int, help='时长（分钟）')
    exercise_parser.add_argument('--calories', '-c', type=int, required=True, help='消耗卡路里')

    # today 子命令
    today_parser = subparsers.add_parser('today', help='查看今日记录')
    today_parser.add_argument('--summary', '-s', action='store_true', help='只显示汇总')

    # history 子命令
    history_parser = subparsers.add_parser('history', help='查看历史记录')
    history_parser.add_argument('days', type=int, nargs='?', default=7, help='查看最近N天（默认7天）')

    # summary 子命令
    summary_parser = subparsers.add_parser('summary', help='查看指定日期汇总')
    summary_parser.add_argument('date', nargs='?', help='日期（YYYY-MM-DD），默认今天')

    # stats 子命令
    subparsers.add_parser('stats', help='查看统计信息')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    db = Database()

    if args.command == 'add-food':
        add_food(db, args.food, args.amount, args.calories)
    elif args.command == 'add-exercise':
        add_exercise(db, args.type, args.duration, args.calories)
    elif args.command == 'today':
        show_today(db, args.summary)
    elif args.command == 'history':
        show_history(db, args.days)
    elif args.command == 'summary':
        show_summary(db, args.date)
    elif args.command == 'stats':
        show_stats(db)

if __name__ == '__main__':
    main()
