#!/usr/bin/env python3
"""
财经日报 - 带 AI 智能分析
使用 DeepSeek V3 API
"""

import os
import requests
from datetime import datetime
from openai import OpenAI

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-87e5f7381cbd44b1839ab79574299594")
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=DEEPSEEK_API_KEY,
)

def get_us_market():
    """获取美股数据 (模拟数据，实际需要代理访问)"""
    # 模拟数据 - 实际环境替换为真实 API
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "indices": {
            "道琼斯": {"price": 38756.12, "change": +0.56},
            "纳斯达克": {"price": 16012.33, "change": +1.23},
            "标普500": {"price": 5123.45, "change": +0.89},
        },
        "top_gainers": [
            {"symbol": "NVDA", "name": "英伟达", "change": +5.67},
            {"symbol": "TSLA", "name": "特斯拉", "change": +3.45},
            {"symbol": "AAPL", "name": "苹果", "change": +2.12},
        ],
        "top_losers": [
            {"symbol": "META", "name": "Meta", "change": -1.23},
            {"symbol": "GOOGL", "name": "谷歌", "change": -0.89},
        ]
    }

def get_fx_rates():
    """获取汇率数据"""
    # 模拟数据
    return {
        "USD/CNY": 7.2456,
        "EUR/CNY": 7.8912,
        "GBP/CNY": 9.2345,
        "JPY/CNY": 0.0487,
    }

def ai_analyze(market_data, fx_data):
    """使用 DeepSeek V3 分析市场数据"""
    
    prompt = f"""
你是财经分析师，请分析以下市场数据，给出简短点评（100字以内）：

【美股表现】
道琼斯: {market_data['indices']['道琼斯']['change']:+.2f}%
纳斯达克: {market_data['indices']['纳斯达克']['change']:+.2f}%
标普500: {market_data['indices']['标普500']['change']:+.2f}%

【领涨股】
{', '.join([f"{g['name']}({g['change']:+.2f}%)" for g in market_data['top_gainers']])}

【领跌股】
{', '.join([f"{l['name']}({l['change']:+.2f}%)" for l in market_data['top_losers']])}

【汇率】
美元/人民币: {fx_data['USD/CNY']}

请给出：
1. 市场整体情绪（乐观/谨慎/悲观）
2. 一句话点评
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI 分析暂时不可用: {str(e)}"

def generate_report():
    """生成完整报告"""
    print("📊 正在获取市场数据...")
    market = get_us_market()
    fx = get_fx_rates()
    
    print("🤖 正在 AI 分析...")
    analysis = ai_analyze(market, fx)
    
    # 生成报告
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━
📈 财经日报 | {market['date']}
━━━━━━━━━━━━━━━━━━━━━━━━

【美股收盘】
道琼斯 {market['indices']['道琼斯']['price']:,.2f} ({market['indices']['道琼斯']['change']:+.2f}%)
纳斯达克 {market['indices']['纳斯达克']['price']:,.2f} ({market['indices']['纳斯达克']['change']:+.2f}%)
标普500 {market['indices']['标普500']['price']:,.2f} ({market['indices']['标普500']['change']:+.2f}%)

【涨幅榜】
🚀 {market['top_gainers'][0]['name']}({market['top_gainers'][0]['symbol']}) {market['top_gainers'][0]['change']:+.2f}%
📈 {market['top_gainers'][1]['name']}({market['top_gainers'][1]['symbol']}) {market['top_gainers'][1]['change']:+.2f}%

【汇率】
美元/人民币: {fx['USD/CNY']}
欧元/人民币: {fx['EUR/CNY']}

━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI 点评
{analysis}
━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # 保存到文件
    with open("daily_report.txt", "w") as f:
        f.write(report)
    print("\n✅ 报告已保存到 daily_report.txt")
