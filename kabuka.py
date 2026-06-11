import requests
import yfinance as yf
import schedule
import time

LINE_TOKEN = "your_token_here"
USER_ID = "your_user_id_here"


stocks = {
    "NTT": "9432.T",
    "ソフトバンク": "9434.T",
    "トヨタ": "7203.T",
    "イオン": "8267.T"
}

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

def check_stocks():
    alerts = []
    message = "📈 本日の株価\n\n"
    lines = []

    for name, code in stocks.items():
        ticker = yf.Ticker(code)
        hist = ticker.history(period="2d")
        yesterday = hist["Close"].iloc[0]
        today = hist["Close"].iloc[1]
        change = (today - yesterday) / yesterday * 100
        lines.append(f"{name}：{today:.0f}円（前日比：{change:+.2f}%）")
        if change <= -10:
            alerts.append(f"⚠️ {name}が{change:.2f}%下落しています！")

    message += "\n".join(lines)
    if alerts:
        message += "\n\n" + "\n".join(alerts)
    
    send_line_message(message)
    print("チェック完了！")

# 5分ごとにチェック（アラートのみ）
def check_alerts():
    for name, code in stocks.items():
        ticker = yf.Ticker(code)
        hist = ticker.history(period="2d")
        yesterday = hist["Close"].iloc[0]
        today = hist["Close"].iloc[1]
        change = (today - yesterday) / yesterday * 100
        if change <= -10:
            send_line_message(f"⚠️ {name}が{change:.2f}%下落しています！")
    print("アラートチェック完了！")

# 朝9時に株価まとめ送信
def morning_report():
    message = "📈 本日の株価\n\n"
    lines = []
    for name, code in stocks.items():
        ticker = yf.Ticker(code)
        hist = ticker.history(period="2d")
        yesterday = hist["Close"].iloc[0]
        today = hist["Close"].iloc[1]
        change = (today - yesterday) / yesterday * 100
        lines.append(f"{name}：{today:.0f}円（前日比：{change:+.2f}%）")
    message += "\n".join(lines)
    send_line_message(message)
    print("朝レポート送信完了！")

# スケジュール設定
schedule.every(5).minutes.do(check_alerts)
schedule.every().day.at("09:00").do(morning_report)

print("監視開始！")
morning_report()  # 起動時に1回確認

while True:
    schedule.run_pending()
    time.sleep(1)
