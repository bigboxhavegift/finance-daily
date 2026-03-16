"""
数据获取模块 - 期货数据
"""

import yfinance as yf
import akshare as ak
import pandas as pd


class FuturesData:
    """期货数据获取"""
    
    @staticmethod
    def get_global_commodities():
        """获取全球大宗商品期货"""
        try:
            commodities = {
                "GC=F": "黄金",
                "CL=F": "WTI原油",
                "SI=F": "白银",
                "HG=F": "铜",
                "NG=F": "天然气",
            }
            
            result = {}
            for symbol, name in commodities.items():
                try:
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
                except:
                    pass
            return result
        except Exception as e:
            print(f"获取全球大宗失败: {e}")
            return {}
    
    @staticmethod
    def get_china_futures():
        """获取中国期货数据"""
        try:
            # 获取主力合约
            df = ak.futures_zh_spot()
            
            # 关注的主要品种
            target = ["螺纹钢", "铁矿石", "焦炭", "焦煤", "沪铜", "沪金", "沪银", 
                      "原油", "燃油", "橡胶", "PTA", "甲醇", "豆粕", "玉米", "棕榈油"]
            
            result = {}
            for _, row in df.iterrows():
                name = row['品种']
                if any(t in name for t in target):
                    if name not in result:  # 只取主力合约
                        result[name] = {
                            "price": float(row['最新价']),
                            "change": float(row['涨跌']),
                            "change_pct": float(row['涨跌幅']),
                        }
            return result
        except Exception as e:
            print(f"获取中国期货失败: {e}")
            return {}


if __name__ == "__main__":
    # 测试
    futures = FuturesData()
    print("全球大宗:", futures.get_global_commodities())
    print("中国期货:", futures.get_china_futures())
