from flask import Flask, request, abort
import random
import os
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def get_cat_news():
    api_key = "33c36db0c82d4682b9cbf99a226e60f5"
    url = "https://newsapi.org/v2/everything"
    query = "猫"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "ja",
        "sortBy": "publishedAt",
        "pageSize": 1,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["totalResults"] > 0:
            article = data["articles"][0]
            title = article["title"]
            url = article["url"]
            return f"最新の猫ニュースにゃ: {title}にゃ\n詳細はこちらにゃ: {url}にゃ"
        else:
            return "猫に関する最新のニュースが見つかりませんでしたにゃ。"
    else:
        return "ニュースを取得できませんでしたにゃ。後でもう一度試してくださいにゃ。"


def cat_response(text):
    responses = [
        # ...
        "最新の猫ニュースを教えて",
    ]

    keywords = [
        # ...
        "猫ニュース",
    ]

    if "猫ニュース" in text:
        return get_cat_news()
    elif any(keyword in text for keyword in keywords):
        return random.choice(responses)
    else:
        return random.choice(responses_else)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    response = cat_response(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response))

if __name__ == "__main__":
    app.run()
