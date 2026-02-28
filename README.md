# CalTrack - 卡路里追踪工具

一个简单的命令行工具，用于记录每日卡路里摄入和运动消耗。

## 功能

- 记录食物摄入（食物名称、数量、卡路里）
- 记录运动消耗（运动类型、时长、卡路里）
- 查看今日记录
- 查看历史记录
- 统计每日净摄入
- 查看总体统计

## 安装

无需安装额外依赖，只需要 Python 3.x。

```bash
cd caltrack
chmod +x caltrack.py
```

## 使用方法

### 添加食物摄入

```bash
python caltrack.py add-food 鸡胸肉 150g --calories 200
```

### 添加运动消耗

```bash
python caltrack.py add-exercise 跑步 30 --calories 300
```

### 查看今日记录

```bash
python caltrack.py today
```

只显示汇总：

```bash
python caltrack.py today --summary
```

### 查看历史记录

```bash
python caltrack.py history 7
```

### 查看指定日期汇总

```bash
python caltrack.py summary 2026-02-28
```

### 查看统计信息

```bash
python caltrack.py stats
```

## 技术栈

- Python 3.x
- SQLite3（内置）

## 许可

MIT License
