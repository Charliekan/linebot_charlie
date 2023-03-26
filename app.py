from flask import Flask, request, abort
import random  # randomモジュールをインポート

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

#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#@app.route("/")
#def test():
#    return "Charlie"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    response = cat_response(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response))

if __name__ == "__main__":
    app.run()