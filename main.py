import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from snownlp import SnowNLP
import random

# 🚨🚨🚨 这里填你的 PushPlus Token 🚨🚨🚨
PUSH_TOKEN = "8f15f31292c642c9a8eb3c5fd15cd7bb" 

def analyze_emoji(text):
    try:
        s = SnowNLP(text)
        score = s.sentiments
        if score > 0.6: return "🎉", score
        elif score < 0.3: return "😱", score
        else: return "😐", score
    except:
        return "🤖", 0.5

def get_smart_news():
    url = "https://s.weibo.com/top/summary"
    
    # 💎 关键修改：加上了超级伪装 (Cookie + User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": "SUB=_2AkMSb-9Af8NxqwJRmP0SzGvhao11ywHEieKkeM_PJRMxHRl-yT9kqmkbtRB6PO6N_Rc_l6fXf1kI0o4X8XzQ1A..;"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('td', class_='td-02')
        
        china_time = datetime.utcnow() + timedelta(hours=8)
        time_str = china_time.strftime("%H:%M")
        
        msg = f"【☁️ 云端哨兵 {time_str}】\n"
        
        # 如果真的没抓到，给一个提示
        if not items:
            return f"【☁️ 云端哨兵 {time_str}】\n❌ 微博反爬虫拦截，需要更新 Cookie。"
            
        for index, item in enumerate(items[:5]):
            # 有时候第一条是广告，没有链接，加个判断防止报错
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.text.strip()
                emoji, score = analyze_emoji(title)
                msg += f"{index+1}. {emoji} {title}\n"
                
        return msg
    except Exception as e:
        return f"❌ 错误: {str(e)}"

def send_wechat(content):
    url = "http://www.pushplus.plus/send"
    data = {"token": PUSH_TOKEN, "title": "☁️ 云端情报", "content": content, "template": "txt"}
    requests.post(url, json=data)

if __name__ == "__main__":
    print("🚀 哨兵启动...")
    news = get_smart_news()
    print(news) 
    send_wechat(news)
    print("✅ 任务完成")
