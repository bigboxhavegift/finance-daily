#!/usr/bin/env python3
"""
财经日报 - 带 AI 智能分析
真实数据源 + DeepSeek V3 API
"""

import os
import requests
import pandas as pd
from datetime import datetime
from openai import OpenAI

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-87e5f7381cbd44b1839ab79574299594")
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=DEEPSEEK_API_KEY,
)

def get_fx_rates():
    """获取真实汇率数据 (优先使用中国银行数据)"""
    try:
        import akshare as ak
        # 获取人民币汇率中间价（中国银行数据，更准确）
        df = ak.currency_boc_safe()
        latest = df.iloc[-1]
        
        # 中行数据是 100 外币兑换人民币，需要除以 100
        return {
            "USD/CNY": round(latest["美元"] / 100, 4),
            "EUR/CNY": round(latest["欧元"] / 100, 4),
            "GBP/CNY": round(latest["英镑"] / 100, 4) if not pd.isna(latest["英镑"]) else 0,
            "JPY/CNY": round(latest["日元"] / 100 / 100, 4),  # 日元是 100 单位
        }
    except Exception as e:
        print(f"⚠️ 中行汇率获取失败: {e}，尝试备用 API...")
        
        # 备用方案：使用免费汇率 API
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("rates"):
                usd_cny = data["rates"]["CNY"]
                return {
                    "USD/CNY": round(usd_cny, 4),
                    "EUR/CNY": round(usd_cny / data["rates"]["EUR"], 4),
                }
        except Exception as e2:
            print(f"⚠️ 备用汇率 API 失败: {e2}")
        
        return {"USD/CNY": 7.2456, "EUR/CNY": 7.8912}

def get_cn_market():
    """获取A股数据 (akshare 免费)"""
    try:
        import akshare as ak
        
        # 获取A股主要指数
        df = ak.stock_zh_index_spot_sina()
        
        indices = {}
        for name in ["上证指数", "深证成指", "创业板指", "科创50"]:
            row = df[df["名称"] == name]
            if not row.empty:
                price = float(row["最新价"].values[0])
                change = float(row["涨跌幅"].values[0])
                indices[name] = {"price": price, "change": change}
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "indices": indices,
            "market": "A股"
        }
    except Exception as e:
        print(f"⚠️ A股数据获取失败: {e}")
        return None

def get_us_market():
    """获取美股数据 (Alpha Vantage API)"""
    
    # 从环境变量或 .env 文件读取 API key
    alpha_vantage_key = os.environ.get("ALPHA_VANTAGE_KEY")
    
    # 尝试从 .env 文件读取
    if not alpha_vantage_key:
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("ALPHA_VANTAGE_KEY="):
                        alpha_vantage_key = line.split("=", 1)[1].strip()
                        break
    
    if not alpha_vantage_key:
        print("  ⚠️ 美股数据需要配置 ALPHA_VANTAGE_KEY")
        print("     注册免费 API: https://www.alphavantage.co/support/#api-key")
        return {"date": datetime.now().strftime("%Y-%m-%d"), "indices": {}, "market": "美股"}
    
    # 使用 ETF 代表指数（Alpha Vantage 免费版不支持直接查询指数）
    etfs = {
        "SPY": "标普500",
        "QQQ": "纳斯达克",
        "DIA": "道琼斯"
    }
    
    indices_data = {}
    
    try:
        for symbol, name in etfs.items():
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={alpha_vantage_key}"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                price = float(quote["05. price"])
                change_pct = float(quote["10. change percent"].replace("%", ""))
                indices_data[name] = {"price": price, "change": change_pct}
            
            # Alpha Vantage 免费版有频率限制，每次调用间隔 0.5 秒
            import time
            time.sleep(0.5)
        
        if indices_data:
            print(f"  ✓ 美股数据: Alpha Vantage ({len(indices_data)} 个指数)")
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "indices": indices_data,
                "market": "美股"
            }
    except Exception as e:
        print(f"  ⚠️ 美股数据获取失败: {e}")
    
    return {"date": datetime.now().strftime("%Y-%m-%d"), "indices": {}, "market": "美股"}

def ai_analyze(cn_data, us_data, fx_data):
    """使用 DeepSeek V3 分析市场数据"""
    
    # 构建分析提示
    prompt_parts = ["你是财经分析师，请分析以下市场数据，给出简短点评（150字以内）：\n"]
    
    # A股数据
    if cn_data and cn_data["indices"]:
        prompt_parts.append("\n【A股表现】")
        for name, data in cn_data["indices"].items():
            prompt_parts.append(f"{name}: {data['change']:+.2f}%")
    
    # 美股数据
    if us_data and us_data["indices"]:
        prompt_parts.append("\n\n【美股表现】")
        for name, data in us_data["indices"].items():
            if data["price"] > 0:
                prompt_parts.append(f"{name}: {data['change']:+.2f}%")
    
    # 汇率数据
    prompt_parts.append("\n\n【汇率】")
    prompt_parts.append(f"美元/人民币: {fx_data['USD/CNY']}")
    prompt_parts.append(f"欧元/人民币: {fx_data['EUR/CNY']}")
    
    prompt_parts.append("\n\n请给出：\n1. 市场整体情绪（乐观/谨慎/悲观）\n2. 关键观察点（1-2个）\n3. 一句话点评")
    
    prompt = "\n".join(prompt_parts)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI 分析暂时不可用: {str(e)}"

def generate_report():
    """生成完整报告"""
    print("📊 正在获取市场数据...")
    
    # 获取各类数据
    fx = get_fx_rates()
    print(f"  ✓ 汇率数据: USD/CNY = {fx['USD/CNY']}")
    
    cn_data = get_cn_market()
    if cn_data and cn_data["indices"]:
        print(f"  ✓ A股数据: {len(cn_data['indices'])} 个指数")
    
    us_data = get_us_market()
    
    print("\n🤖 正在 AI 分析...")
    analysis = ai_analyze(cn_data, us_data, fx)
    
    # 生成报告
    report_lines = [
        "━" * 30,
        f"📈 财经日报 | {datetime.now().strftime('%Y-%m-%d')}",
        "━" * 30,
    ]
    
    # A股部分
    if cn_data and cn_data["indices"]:
        report_lines.append("\n【A股收盘】")
        for name, data in cn_data["indices"].items():
            emoji = "📈" if data["change"] > 0 else "📉"
            report_lines.append(f"{emoji} {name} {data['price']:,.2f} ({data['change']:+.2f}%)")
    
    # 美股部分
    if us_data and us_data["indices"]:
        report_lines.append("\n【美股收盘】")
        for name, data in us_data["indices"].items():
            if data["price"] > 0:
                emoji = "📈" if data["change"] > 0 else "📉"
                report_lines.append(f"{emoji} {name} {data['price']:,.2f} ({data['change']:+.2f}%)")
    else:
        report_lines.append("\n【美股】")
        report_lines.append("⚠️ 数据暂时不可用（交易时间外或网络问题）")
    
    # 汇率部分
    report_lines.append("\n【汇率】")
    report_lines.append(f"💵 美元/人民币: {fx['USD/CNY']}")
    report_lines.append(f"💶 欧元/人民币: {fx['EUR/CNY']}")
    
    # AI分析
    report_lines.append("\n" + "━" * 30)
    report_lines.append("🤖 AI 点评")
    report_lines.append(analysis)
    report_lines.append("━" * 30)
    
    report = "\n".join(report_lines)
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # 保存到文件
    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n✅ 报告已保存到 daily_report.txt")
