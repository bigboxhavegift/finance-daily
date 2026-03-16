"""
金融日报配置文件
"""

# GitHub 配置
GITHUB_USER = "bigboxhavegift"
REPO_NAME = "finance-daily"
PAGES_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/"

# 数据更新时间 (UTC+8)
MORNING_UPDATE = "08:00"  # 早盘分析
EVENING_UPDATE = "19:00"  # 晚盘总结

# 市场配置
MARKETS = {
    "china_stocks": {
        "name": "A股",
        "indices": ["000001.SH", "399001.SZ", "000300.SH"],  # 上证、深证、沪深300
        "top_stocks": 10,  # 关注前10大市值
    },
    "us_stocks": {
        "name": "美股",
        "indices": ["^DJI", "^GSPC", "^IXIC"],  # 道琼斯、标普、纳指
        "top_stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
    },
    "hk_stocks": {
        "name": "港股",
        "indices": ["^HSI"],  # 恒生指数
        "top_stocks": ["0700.HK", "9988.HK", "0941.HK"],  # 腾讯、阿里、中国移动
    },
    "global_futures": {
        "name": "全球大宗",
        "commodities": ["GC=F", "CL=F", "SI=F", "HG=F"],  # 黄金、原油、白银、铜
    },
    "china_futures": {
        "name": "中国期货",
        "exchanges": ["SHFE", "DCE", "CZCE", "CFFEX"],
    },
}

# 经济指标关注点
ECONOMIC_INDICATORS = {
    "china": ["PMI", "CPI", "PPI", "GDP", "M2", "利率"],
    "us": ["非农", "CPI", "PPI", "GDP", "美联储利率", "失业率"],
    "global": ["美元指数", "美债收益率", "VIX恐慌指数"],
}

# 新闻关键词
NEWS_KEYWORDS = [
    "美联储", "央行", "利率", "通胀",
    "GDP", "PMI", "就业", "贸易",
    "地缘政治", "战争", "制裁",
    "原油", "黄金", "大宗商品",
]
