from flask import Flask, request, abort

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

line_bot_api = LineBotApi('l+ruA4eNSuDv+4lxdnPF/JY81N3pshr/o80pc5k1oI92YdJpZ36L3oEunYW8NlBt2noUuNUI5E1JSSf5djAPeCKsXbsLWZrDNP6L4AyRpQlEH1A+9Vpdy/fSSu9mKZq4w1diAKxrgZWvKEWrL1YXOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('842a65fc186f819ddc503f054e44682b')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
