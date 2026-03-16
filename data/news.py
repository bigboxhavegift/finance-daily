"""
数据获取模块 - 新闻数据
"""

import akshare as ak
import feedparser
from datetime import datetime


class NewsData:
    """新闻数据获取"""
    
    # RSS 源
    RSS_FEEDS = [
        "https://news.cnstock.com/rss/news.xml",  # 上证报
        "https://www.yicai.com/rss/rss.html",  # 一财
        "https://www.ftchinese.com/rss/feed",  # FT中文
    ]
    
    @staticmethod
    def get_financial_news(keywords=None):
        """获取财经新闻"""
        if keywords is None:
            keywords = ["美联储", "央行", "利率", "通胀", "GDP", "PMI"]
        
        news_list = []
        
        for feed_url in NewsData.RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    
                    # 检查关键词
                    if any(kw in title or kw in summary for kw in keywords):
                        news_list.append({
                            "title": title,
                            "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                            "link": entry.get('link', ''),
                            "published": entry.get('published', ''),
                        })
            except Exception as e:
                print(f"获取RSS失败 {feed_url}: {e}")
        
        return news_list[:20]  # 返回前20条


if __name__ == "__main__":
    # 测试
    news = NewsData()
    articles = news.get_financial_news()
    for a in articles[:5]:
        print(f"- {a['title']}")
