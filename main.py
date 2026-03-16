"""
金融日报主程序
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 导入数据模块
from data.stocks import StockData
from data.futures import FuturesData
from data.news import NewsData

# 导入分析模块
from analysis.economic import EconomicCycleAnalysis
from analysis.geopolitical import GeopoliticalAnalysis
from analysis.trade import TradeAnalysis

# 配置
from config import PAGES_URL


def generate_report():
    """生成金融日报"""
    print("=" * 50)
    print("金融日报生成中...")
    print("=" * 50)
    
    # 获取数据
    print("\n📊 获取市场数据...")
    stock = StockData()
    futures = FuturesData()
    news = NewsData()
    
    china_stocks = stock.get_china_index()
    us_stocks = stock.get_us_index()
    hk_stocks = stock.get_hk_index()
    commodities = futures.get_global_commodities()
    china_futures = futures.get_china_futures()
    news_list = news.get_financial_news()
    
    print(f"  - A股指数: {len(china_stocks)} 个")
    print(f"  - 美股指数: {len(us_stocks)} 个")
    print(f"  - 港股指数: {len(hk_stocks)} 个")
    print(f"  - 全球大宗: {len(commodities)} 个")
    print(f"  - 中国期货: {len(china_futures)} 个")
    print(f"  - 相关新闻: {len(news_list)} 条")
    
    # 生成分析
    print("\n🔍 生成分析报告...")
    economic = EconomicCycleAnalysis()
    geopolitical = GeopoliticalAnalysis()
    trade = TradeAnalysis()
    
    economic_analysis = economic.generate_report()
    
    # 从新闻分析地缘政治
    geopolitical_risks = geopolitical.analyze_from_news(news_list)
    geopolitical_analysis = geopolitical.generate_report(geopolitical_risks)
    
    trade_analysis = trade.generate_report({
        'usd_index': 104.5,
        'bdi': 1800
    })
    
    # 渲染 HTML
    print("\n📄 渲染网页...")
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    
    html = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M"),
        china_stocks=china_stocks,
        us_stocks=us_stocks,
        hk_stocks=hk_stocks,
        commodities=commodities,
        china_futures=china_futures,
        news_list=news_list,
        economic_analysis=economic_analysis,
        geopolitical_analysis=geopolitical_analysis,
        trade_analysis=trade_analysis,
    )
    
    # 保存输出
    output_path = "output/docs/index.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告已生成: {output_path}")
    print(f"🌐 访问地址: {PAGES_URL}")
    
    return html


def send_to_feishu(html_path: str):
    """发送到飞书"""
    # TODO: 实现飞书推送
    print(f"\n📱 飞书推送: {PAGES_URL}")
    pass


if __name__ == "__main__":
    generate_report()
