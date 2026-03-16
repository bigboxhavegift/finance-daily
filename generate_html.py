#!/usr/bin/env python3
"""
财经日报 - 生成响应式网页
"""

import os
import json
from datetime import datetime
from openai import OpenAI

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-87e5f7381cbd44b1839ab79574299594")
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=DEEPSEEK_API_KEY,
) if DEEPSEEK_API_KEY else None

def get_us_market():
    """获取美股数据"""
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
    return {
        "USD/CNY": 7.2456,
        "EUR/CNY": 7.8912,
        "GBP/CNY": 9.2345,
        "JPY/CNY": 0.0487,
    }

def ai_analyze(market_data, fx_data):
    """AI 分析市场数据"""
    if not client:
        return "⚠️ AI 分析需要配置 DEEPSEEK_API_KEY"
    
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

def generate_html(market, fx, analysis):
    """生成响应式 HTML"""
    
    # 格式化涨跌幅
    def format_change(change):
        color = "#10b981" if change >= 0 else "#ef4444"
        symbol = "↑" if change >= 0 else "↓"
        return f'<span style="color: {color}">{symbol} {abs(change):.2f}%</span>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经日报 | {market['date']}</title>
    <meta name="description" content="每日财经市场数据与 AI 分析">
    <meta name="theme-color" content="#1e293b">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: clamp(1.8rem, 5vw, 2.5rem);
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        .date {{
            color: #94a3b8;
            font-size: 0.95rem;
        }}
        
        .card {{
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .card-title {{
            font-size: 1.1rem;
            color: #60a5fa;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .index-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .index-item {{
            background: rgba(15, 23, 42, 0.4);
            padding: 16px;
            border-radius: 12px;
        }}
        
        .index-name {{
            color: #94a3b8;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }}
        
        .index-value {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .index-change {{
            font-size: 1rem;
        }}
        
        .stock-list {{
            list-style: none;
        }}
        
        .stock-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }}
        
        .stock-item:last-child {{
            border-bottom: none;
        }}
        
        .stock-name {{
            font-weight: 500;
        }}
        
        .stock-symbol {{
            color: #64748b;
            font-size: 0.85rem;
            margin-left: 8px;
        }}
        
        .fx-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }}
        
        .fx-item {{
            background: rgba(15, 23, 42, 0.4);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .fx-pair {{
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }}
        
        .fx-rate {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .analysis {{
            line-height: 1.7;
            color: #cbd5e1;
        }}
        
        .update-time {{
            text-align: center;
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 40px;
        }}
        
        @media (max-width: 600px) {{
            .card {{
                padding: 16px;
            }}
            
            .index-value {{
                font-size: 1.2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 财经日报</h1>
            <p class="date">{market['date']}</p>
        </header>
        
        <div class="card">
            <div class="card-title">📊 美股收盘</div>
            <div class="index-grid">
                <div class="index-item">
                    <div class="index-name">道琼斯</div>
                    <div class="index-value">{market['indices']['道琼斯']['price']:,.2f}</div>
                    <div class="index-change">{format_change(market['indices']['道琼斯']['change'])}</div>
                </div>
                <div class="index-item">
                    <div class="index-name">纳斯达克</div>
                    <div class="index-value">{market['indices']['纳斯达克']['price']:,.2f}</div>
                    <div class="index-change">{format_change(market['indices']['纳斯达克']['change'])}</div>
                </div>
                <div class="index-item">
                    <div class="index-name">标普500</div>
                    <div class="index-value">{market['indices']['标普500']['price']:,.2f}</div>
                    <div class="index-change">{format_change(market['indices']['标普500']['change'])}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🚀 涨幅榜</div>
            <ul class="stock-list">
                {''.join([f'<li class="stock-item"><span><span class="stock-name">{s["name"]}</span><span class="stock-symbol">{s["symbol"]}</span></span><span>{format_change(s["change"])}</span></li>' for s in market['top_gainers']])}
            </ul>
        </div>
        
        <div class="card">
            <div class="card-title">💸 汇率</div>
            <div class="fx-grid">
                {''.join([f'<div class="fx-item"><div class="fx-pair">{pair}</div><div class="fx-rate">{rate:.4f}</div></div>' for pair, rate in fx.items()])}
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🤖 AI 点评</div>
            <div class="analysis">{analysis}</div>
        </div>
        
        <p class="update-time">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 由 DeepSeek V3 提供分析</p>
    </div>
</body>
</html>'''
    
    return html

def main():
    print("📊 获取市场数据...")
    market = get_us_market()
    fx = get_fx_rates()
    
    print("🤖 AI 分析中...")
    analysis = ai_analyze(market, fx)
    
    print("🌐 生成网页...")
    html = generate_html(market, fx, analysis)
    
    # 保存 HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 网页已生成: index.html")

if __name__ == "__main__":
    main()
