import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from snownlp import SnowNLP
import os

# 🚨 请把你的 Token 填在下面这个引号里！
PUSH_TOKEN = os.environ.get("8f15f31292c642c9a8eb3c5fd15cd7bb")

def analyze_emoji(text):
    s = SnowNLP(text)
    score = s.sentiments
    if score > 0.6: return "🎉", score
    elif score < 0.3: return "😱", score
    else: return "😐", score

def get_smart_news():
    url = "https://s.weibo.com/top/summary"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('td', class_='td-02')
        
        # 时区修正 (GitHub服务器在国外)
        china_time = datetime.utcnow() + timedelta(hours=8)
        time_str = china_time.strftime("%H:%M")
        
        msg = f"【☁️ 云端哨兵 {time_str}】\n"
        for index, item in enumerate(items[:5]):
            title = item.find('a').text.strip()
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
    send_wechat(news)
    print("✅ 任务完成，准备休眠。")
