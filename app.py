from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage



app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "dyq6khZiHk8OlnAXqU/LVpOKfhFiDkyOIr4V8/rJusi4p5ItvRUNalwc6RIcYj8pSyS5xuVXFENY1VoCLYPcv8WLSNfVxIcQfV3/WO5jrrvw3ovDf6rCzGMaKRGtoCzk3ZybaUPYShBwPFnz5EvXOQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "9fca34fa06fd1fd4d674ed6f6ce10233"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def hello_world():
  return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

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
  app.run()