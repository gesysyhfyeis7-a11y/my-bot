import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from snownlp import SnowNLP

# 🚨🚨🚨 必须修改这里！填入你在 PushPlus 拿到的 Token 🚨🚨🚨
# 比如 PUSH_TOKEN = "abc123456789"
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
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('td', class_='td-02')
        
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
    resp = requests.post(url, json=data)
    print("推送结果:", resp.text)

if __name__ == "__main__":
    print("🚀 哨兵启动...")
    news = get_smart_news()
    send_wechat(news)
    print("✅ 任务完成")
