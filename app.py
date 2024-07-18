from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, request, abort
import random

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

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

def cat_response(text):
    responses = [
        "お腹すいたにゃー",
        "あそびたいにゃー",
        "だいすきにゃ",
        "ちゃーはいいこだにゃ",
        "ごはんはよはよ",
        "(*ΦωΦ*)",
        "ニャンパス",
        "ニャンニャン",
        "すりすり",
        "スリスリニャン",
        "トイレそろそろくさいにゃ",
        "ごはんまだかにゃ",
        "にゃーーーーーーーーー",
        "にゃにゃにゃんにゃんにゃん",
        "ねむいちゃ",
        "ちゃーは暇です",
        "かまって〜〜〜〜",
        "にゃんにゃんにゃにゃにゃにゃんにゃんにゃにゃーにゃにゃんにゃんにゃにゃにゃにゃんーにゃんにゃにゃにゃ",
        "ちゅーるちゅーるちゃおちゅーるー",
        "お仕事ふぁいとだにゃ",

    ]

    keywords = ["ちゃ","ちゃんとご飯食べてね","ごはんもう全部食べたの","ご飯たべた","いまなにしてるの","なにしてるの","なにしてるのー","あいたい","だいすき","らぶ","かわいい","ちゃーりー","チャーリー","チャー","お腹すいた？","おなかすいた？","もうすぐ帰るよ","もうすぐかえるよ","まっててね", "ちゃーちゃん", "ちゃー", "いまかえるよ", "まっててね", "にゃ", "にゃん", "にゃー"]
    if any(keyword in text for keyword in keywords):
        return random.choice(responses)
    else:
        return "にゃーん"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    response = cat_response(text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)