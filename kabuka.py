import requests
import yfinance as yf

import requests
import yfinance as yf

LINE_TOKEN = ""
USER_ID = ""


stocks = {
    "NTT": "9432.T",
    "ソフトバンク": "9434.T",
    "トヨタ": "7203.T",
    "イオン": "8267.T"
}

def get_stock_price(name, code):
    ticker = yf.Ticker(code)
    price = ticker.fast_info["lastPrice"]
    return f"{name}：{price:.0f}円"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)

message = "📈 本日の株価\n\n"
message += "\n".join([get_stock_price(name, code) for name, code in stocks.items()])
send_line_message(message)
print("送信完了！")