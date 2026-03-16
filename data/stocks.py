"""
数据获取模块 - 股票数据
"""

import yfinance as yf
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


class StockData:
    """股票数据获取"""
    
    @staticmethod
    def get_us_index():
        """获取美股指数"""
        try:
            # 道琼斯、标普500、纳斯达克
            indices = {
                "^DJI": "道琼斯",
                "^GSPC": "标普500",
                "^IXIC": "纳斯达克"
            }
            
            result = {}
            for symbol, name in indices.items():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                if len(hist) >= 2:
                    latest = hist.iloc[-1]
                    prev = hist.iloc[-2]
                    change_pct = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
                    result[name] = {
                        "price": round(latest['Close'], 2),
                        "change": round(latest['Close'] - prev['Close'], 2),
                        "change_pct": round(change_pct, 2),
                    }
            return result
        except Exception as e:
            print(f"获取美股指数失败: {e}")
            return {}
    
    @staticmethod
    def get_hk_index():
        """获取港股指数"""
        try:
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
            # 使用 akshare 获取 A 股指数
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
    # 测试
    stock = StockData()
    print("美股:", stock.get_us_index())
    print("港股:", stock.get_hk_index())
    print("A股:", stock.get_china_index())
