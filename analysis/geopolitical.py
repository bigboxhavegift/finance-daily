"""
分析模块 - 地缘政治分析
"""

from typing import List, Dict


class GeopoliticalAnalysis:
    """地缘政治分析"""
    
    # 关注的地缘政治主题
    THEMES = [
        "中美关系",
        "俄乌冲突",
        "中东局势",
        "台海局势",
        "朝鲜半岛",
        "欧盟政策",
    ]
    
    def __init__(self):
        self.news_keywords = {
            "中美关系": ["关税", "制裁", "贸易战", "科技战", "芯片"],
            "俄乌冲突": ["俄罗斯", "乌克兰", "北约", "能源"],
            "中东局势": ["以色列", "巴勒斯坦", "伊朗", "石油", "红海"],
        }
    
    def analyze_from_news(self, news_list: List[Dict]) -> Dict:
        """从新闻分析地缘政治风险"""
        risks = {}
        
        for theme, keywords in self.news_keywords.items():
            related_news = []
            for news in news_list:
                title = news.get('title', '')
                summary = news.get('summary', '')
                
                if any(kw in title or kw in summary for kw in keywords):
                    related_news.append(news['title'])
            
            if related_news:
                risks[theme] = {
                    "level": len(related_news),  # 新闻数量作为风险等级
                    "news": related_news[:3],
                }
        
        return risks
    
    def generate_report(self, risks: Dict) -> str:
        """生成地缘政治分析报告"""
        report = """
## 地缘政治分析

### 风险地图

| 地区 | 风险等级 | 重点关注 |
|------|---------|---------|
"""
        
        for theme, data in risks.items():
            level = "🔴 高" if data['level'] > 5 else "🟡 中" if data['level'] > 2 else "🟢 低"
            news = data['news'][0] if data['news'] else "暂无"
            report += f"| {theme} | {level} | {news[:30]}... |\n"
        
        report += """
### 市场影响

[根据风险分析自动生成]
"""
        return report


if __name__ == "__main__":
    gp = GeopoliticalAnalysis()
    # 模拟新闻
    test_news = [
        {"title": "美国对中国芯片制裁升级", "summary": ""},
        {"title": "红海局势紧张影响航运", "summary": ""},
    ]
    risks = gp.analyze_from_news(test_news)
    print(gp.generate_report(risks))
