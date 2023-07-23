from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json
import requests

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

weather_api_key = "c69bb80cbc3a9fd39ad8ca79ec515c1d"


def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"  # 使用公制單位來取得溫度資訊
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"城市：{city}\n天氣：{weather_description}\n溫度：{temperature}°C"
    else:
        return "無法取得天氣資訊，請確認城市名稱是否正確。"
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'fRaRaVF+fn0QkrR+qFo5hitLswTUc6zRAbo+vJ3lLPliO3Ya41lwSaMlPJkUkO3qBkJX1bM1bA4E0ZAATc6RcJ9H2TDteoxiukdtiA3lUK5C9wU7cUpW+xqIPN2nq38NPDgLSb1Txr1uyOEp8622qAdB04t89/1O/w1cDnyilFU='
        secret = 'f7dc1e76d72ce227298061769156efc1'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type == 'text':
            msg = json_data['events'][0]['message']['text']
            if msg.startswith("/weather"):
                city = msg.split("/weather ", 1)[1]
                reply = get_weather(city)
            else:
                reply = "請輸入 /weather 城市名稱 來查詢天氣，例如：/weather Taipei"
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()