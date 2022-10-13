from flask import Flask, request, abort
import os

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



line_bot_api = LineBotApi("dyq6khZiHk8OlnAXqU/LVpOKfhFiDkyOIr4V8/rJusi4p5ItvRUNalwc6RIcYj8pSyS5xuVXFENY1VoCLYPcv8WLSNfVxIcQfV3/WO5jrrvw3ovDf6rCzGMaKRGtoCzk3ZybaUPYShBwPFnz5EvXOQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("9fca34fa06fd1fd4d674ed6f6ce10233")

@app.route("/")
def hello_world():
    return "hello world!"

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT","5000"))
    app.run(host="0.0.0.0", port=port)