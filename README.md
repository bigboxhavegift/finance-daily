# 金融日报系统

每日自动生成金融市场分析报告，并通过 GitHub Pages 发布。

## 功能

- 📈 **市场数据**：A股、美股、港股、全球大宗期货、中国期货
- 🌍 **分析维度**：经济周期、地缘政治、世界贸易
- ⏰ **定时推送**：早 8:00 / 晚 19:00
- 📱 **多端展示**：响应式网页 + 飞书推送

## 技术栈

- Python 3.9+
- yfinance / akshare (数据获取)
- pandas / numpy (数据处理)
- plotly (可视化)
- GitHub Pages (托管)

## 项目结构

```
finance-daily/
├── data/               # 数据获取模块
│   ├── stocks.py       # 股票数据
│   ├── futures.py      # 期货数据
│   └── news.py         # 新闻数据
├── analysis/           # 分析模块
│   ├── economic.py     # 经济周期分析
│   ├── geopolitical.py # 地缘政治分析
│   └── trade.py        # 世界贸易分析
├── templates/          # 网页模板
│   └── report.html     # 报告模板
├── output/             # 输出目录
│   └── docs/           # GitHub Pages
├── config.py           # 配置文件
├── main.py             # 主程序
└── requirements.txt    # 依赖列表
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 作者

@bigboxhavegift
