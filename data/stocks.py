"""
数据获取模块 - 股票数据
支持: Alpha Vantage (美股) / yfinance (港股) / akshare (A股)
"""

import requests
import pandas as pd
from datetime import datetime

# Alpha Vantage API Key
ALPHA_VANTAGE_KEY = "QAQUOPS64YPE6IO5"


class StockData:
    """股票数据获取"""
    
    @staticmethod
    def get_us_index():
        """获取美股指数 (使用 Alpha Vantage)"""
        # 使用 ETF 代理指数
        etf_map = {
            "SPY": "标普500",
            "DIA": "道琼斯", 
            "QQQ": "纳斯达克"
        }
        
        result = {}
        for symbol, name in etf_map.items():
            try:
                url = f"https://www.alphavantage.co/query"
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": ALPHA_VANTAGE_KEY
                }
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()
                
                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    price = float(quote.get("05. price", 0))
                    change = float(quote.get("09. change", 0))
                    change_pct = float(quote.get("10. change percent", "0").replace("%", ""))
                    
                    result[name] = {
                        "price": round(price, 2),
                        "change": round(change, 2),
                        "change_pct": round(change_pct, 2),
                    }
            except Exception as e:
                print(f"获取 {name} 失败: {e}")
        
        return result
    
    @staticmethod
    def get_hk_index():
        """获取港股指数"""
        try:
            import yfinance as yf
            ticker = yf.Ticker("^HSI")
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                latest = hist.iloc[-1]
                prev = hist.iloc[-2]
                change_pct = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
                return {
                    "恒生指数": {
                        "price": round(latest['Close'], 2),
                        "change": round(latest['Close'] - prev['Close'], 2),
                        "change_pct": round(change_pct, 2),
                    }
                }
        except Exception as e:
            print(f"获取港股指数失败: {e}")
        return {}
    
    @staticmethod
    def get_china_index():
        """获取A股指数"""
        try:
            import akshare as ak
            df = ak.stock_zh_index_spot_em(symbol="上证系列指数")
            
            result = {}
            indices = {"上证指数": "000001", "深证成指": "399001", "沪深300": "000300"}
            
            for name, code in indices.items():
                row = df[df['代码'] == code]
                if not row.empty:
                    result[name] = {
                        "price": float(row['最新价'].values[0]),
                        "change": float(row['涨跌额'].values[0]),
                        "change_pct": float(row['涨跌幅'].values[0]),
                    }
            return result
        except Exception as e:
            print(f"获取A股指数失败: {e}")
            return {}


if __name__ == "__main__":
    stock = StockData()
    print("美股:", stock.get_us_index())
    print("港股:", stock.get_hk_index())
    print("A股:", stock.get_china_index())
