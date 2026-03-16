"""
金融日报 - 使用真实数据
"""

import os
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.stocks import StockData
from data.futures import FuturesData
from data.news import NewsData

# 模拟数据（备用）
MOCK_CHINA = {
    "上证指数": {"price": 3256.78, "change": 23.45, "change_pct": 0.72},
    "深证成指": {"price": 10856.32, "change": -45.67, "change_pct": -0.42},
    "沪深300": {"price": 3856.21, "change": 12.34, "change_pct": 0.32},
}

MOCK_HK = {
    "恒生指数": {"price": 17234.56, "change": 234.56, "change_pct": 1.38},
}

MOCK_COMMODITIES = {
    "黄金": {"price": 2156.78, "change_pct": 0.58},
    "WTI原油": {"price": 78.45, "change_pct": -1.54},
    "白银": {"price": 24.89, "change_pct": 1.38},
    "铜": {"price": 3.89, "change_pct": 1.30},
}

MOCK_NEWS = [
    {"title": "美联储维持利率不变，暗示年内可能降息", "link": "#", "published": "2026-03-16"},
    {"title": "中国PMI重回扩张区间，经济复苏迹象显现", "link": "#", "published": "2026-03-16"},
    {"title": "红海局势紧张，国际油价上涨", "link": "#", "published": "2026-03-16"},
]


def generate_report():
    """生成金融日报"""
    print("📊 获取数据...")
    
    stock = StockData()
    
    # 获取真实美股数据
    us_stocks = stock.get_us_index()
    print(f"  ✅ 美股: {len(us_stocks)} 个指数")
    
    # A股和港股使用模拟数据
    china_stocks = MOCK_CHINA
    hk_stocks = MOCK_HK
    commodities = MOCK_COMMODITIES
    
    # 生成 HTML
    print("📄 生成报告...")
    
    html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>金融日报 - {datetime.now().strftime("%Y-%m-%d")}</title>
<style>
body{{font-family:system-ui;background:#1a1a2e;color:#e0e0e0;padding:20px;margin:0}}
.container{{max-width:1200px;margin:0 auto}}
header{{text-align:center;padding:30px 0;border-bottom:1px solid #333;margin-bottom:30px}}
h1{{font-size:2em;color:#fff;margin-bottom:10px}}
.update-time{{color:#888;font-size:0.9em}}
.section{{background:rgba(255,255,255,0.05);border-radius:15px;padding:25px;margin-bottom:25px}}
.section h2{{color:#4fc3f7;border-left:4px solid #4fc3f7;padding-left:15px;margin-bottom:20px}}
h3{{color:#ff9800;margin:20px 0 15px;font-size:1.1em}}
.market-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px}}
.market-card{{background:rgba(0,0,0,0.3);border-radius:10px;padding:20px;text-align:center}}
.market-card h4{{font-size:0.9em;color:#aaa;margin-bottom:10px}}
.market-card .price{{font-size:1.6em;font-weight:bold;color:#fff}}
.change.up{{color:#4caf50;font-size:0.95em;margin-top:5px}}
.change.down{{color:#f44336;font-size:0.95em;margin-top:5px}}
footer{{text-align:center;padding:30px;color:#666;margin-top:30px}}
</style></head>
<body><div class="container">
<header><h1>📈 金融日报</h1>
<div class="update-time">更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | 数据来源：Alpha Vantage</div>
</header>

<section class="section"><h2>🇺🇸 美股市场</h2>
<div class="market-grid">'''
    
    for name, data in us_stocks.items():
        cls = "up" if data["change"] > 0 else "down"
        sign = "+" if data["change"] > 0 else ""
        html += f'''<div class="market-card">
<h4>{name}</h4>
<div class="price">{data["price"]}</div>
<div class="change {cls}">{sign}{data["change"]} ({sign}{data["change_pct"]}%)</div>
</div>'''
    
    html += '''</div></section>

<section class="section"><h2>🇨🇳 A股市场</h2>
<div class="market-grid">'''
    
    for name, data in china_stocks.items():
        cls = "up" if data["change"] > 0 else "down"
        sign = "+" if data["change"] > 0 else ""
        html += f'''<div class="market-card">
<h4>{name}</h4>
<div class="price">{data["price"]}</div>
<div class="change {cls}">{sign}{data["change"]} ({sign}{data["change_pct"]}%)</div>
</div>'''
    
    html += '''</div></section>

<section class="section"><h2>🇭🇰 港股市场</h2>
<div class="market-grid">'''
    
    for name, data in hk_stocks.items():
        cls = "up" if data["change"] > 0 else "down"
        sign = "+" if data["change"] > 0 else ""
        html += f'''<div class="market-card">
<h4>{name}</h4>
<div class="price">{data["price"]}</div>
<div class="change {cls}">{sign}{data["change"]} ({sign}{data["change_pct"]}%)</div>
</div>'''
    
    html += '''</div></section>

<section class="section"><h2>📊 大宗商品</h2>
<div class="market-grid">'''
    
    for name, data in commodities.items():
        cls = "up" if data["change_pct"] > 0 else "down"
        sign = "+" if data["change_pct"] > 0 else ""
        html += f'''<div class="market-card">
<h4>{name}</h4>
<div class="price">{data["price"]}</div>
<div class="change {cls}">{sign}{data["change_pct"]}%</div>
</div>'''
    
    html += '''</div></section>

<footer>
<p>数据来源：Alpha Vantage (美股) | 模拟数据 (A股/港股/大宗)</p>
<p>© 2026 金融日报 | by bigboxhavegift</p>
</footer>
</div></body></html>'''
    
    # 保存
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 报告已生成: docs/index.html")
    return html


if __name__ == "__main__":
    generate_report()
