"""
金融日报测试版 - 使用模拟数据
"""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 模拟数据
MOCK_DATA = {
    "china_stocks": {
        "上证指数": {"price": 3256.78, "change": 23.45, "change_pct": 0.72},
        "深证成指": {"price": 10856.32, "change": -45.67, "change_pct": -0.42},
        "沪深300": {"price": 3856.21, "change": 12.34, "change_pct": 0.32},
    },
    "us_stocks": {
        "道琼斯": {"price": 38956.78, "change": 156.23, "change_pct": 0.40},
        "标普500": {"price": 5123.45, "change": -23.45, "change_pct": -0.46},
        "纳斯达克": {"price": 16123.56, "change": 89.34, "change_pct": 0.56},
    },
    "hk_stocks": {
        "恒生指数": {"price": 17234.56, "change": 234.56, "change_pct": 1.38},
    },
    "commodities": {
        "黄金": {"price": 2156.78, "change": 12.34, "change_pct": 0.58},
        "WTI原油": {"price": 78.45, "change": -1.23, "change_pct": -1.54},
        "白银": {"price": 24.89, "change": 0.34, "change_pct": 1.38},
        "铜": {"price": 3.89, "change": 0.05, "change_pct": 1.30},
        "天然气": {"price": 1.78, "change": 0.05, "change_pct": 2.89},
    },
    "news_list": [
        {"title": "美联储维持利率不变，暗示年内可能降息", "link": "#", "published": "2026-03-16"},
        {"title": "中国PMI重回扩张区间，经济复苏迹象显现", "link": "#", "published": "2026-03-16"},
        {"title": "红海局势紧张，国际油价上涨", "link": "#", "published": "2026-03-16"},
        {"title": "港股科技股反弹，恒生科技指数涨超2%", "link": "#", "published": "2026-03-16"},
        {"title": "美元指数走强，新兴市场货币承压", "link": "#", "published": "2026-03-16"},
    ]
}

ECONOMIC_ANALYSIS = """
## 经济周期分析

### 当前判断

基于主要经济指标，判断当前处于：

- **中国**：经济温和复苏，PMI重回扩张区间，政策支持力度加大
- **美国**：经济软着陆预期增强，通胀逐步回落，利率维持高位

### 关键信号

1. **利率**：中美利差维持高位，资本外流压力仍存
2. **通胀**：中国CPI温和，美国通胀回落至3%以下
3. **就业**：美国失业率维持低位，中国就业形势稳定
4. **制造业**：中国PMI回升至50.2，进入扩张区间

### 投资启示

- 关注内需消费板块机会
- 留意科技股估值修复
- 大宗商品可能震荡整理
"""

GEOPOLITICAL_ANALYSIS = """
## 地缘政治分析

### 风险地图

| 地区 | 风险等级 | 重点关注 |
|------|---------|---------|
| 中美关系 | 🟡 中 | 芯片制裁持续，贸易谈判待观察 |
| 俄乌冲突 | 🟡 中 | 战事持续，能源供应影响减弱 |
| 中东局势 | 🔴 高 | 红海航运受阻，油价波动加剧 |
| 台海局势 | 🟢 低 | 局势平稳，两岸交流恢复 |

### 市场影响

- 能源价格波动：中东风险推高油价
- 航运成本：红海绕行增加运输成本
- 供应链：芯片限制影响科技行业
"""

TRADE_ANALYSIS = """
## 世界贸易分析

### 汇率市场

- **美元指数**：104.5
- **判断**：强势美元
- **影响**：不利于新兴市场，大宗商品承压

### 航运市场

- **BDI指数**：1800
- **判断**：航运景气度中等
- **含义**：全球贸易平稳运行

### 贸易趋势

中国出口逐步恢复，进口需求稳定，贸易顺差维持。

### 投资启示

关注出口导向型企业，留意汇率波动影响。
"""


def generate_test_report():
    """生成测试版报告"""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    
    html = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M"),
        china_stocks=MOCK_DATA["china_stocks"],
        us_stocks=MOCK_DATA["us_stocks"],
        hk_stocks=MOCK_DATA["hk_stocks"],
        commodities=MOCK_DATA["commodities"],
        china_futures={},
        news_list=MOCK_DATA["news_list"],
        economic_analysis=ECONOMIC_ANALYSIS,
        geopolitical_analysis=GEOPOLITICAL_ANALYSIS,
        trade_analysis=TRADE_ANALYSIS,
    )
    
    # 保存输出
    output_path = "output/docs/index.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 测试报告已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_test_report()
