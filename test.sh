#!/bin/bash
# 测试脚本

echo "==================================="
echo "金融日报系统测试"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "1. 测试数据获取模块..."
python3 -c "
from data.stocks import StockData
s = StockData()
print('美股:', s.get_us_index())
"

echo ""
echo "2. 测试期货数据..."
python3 -c "
from data.futures import FuturesData
f = FuturesData()
print('大宗商品:', f.get_global_commodities())
"

echo ""
echo "3. 运行完整报告..."
python3 main.py

echo ""
echo "==================================="
echo "测试完成！"
echo "==================================="
