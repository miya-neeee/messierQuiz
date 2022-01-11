##テスト

#インポートするライブラリ
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os

##WebApplicationFlamework:flask
app = Flask(__name__)

##環境変数からLINE ACCESS TOKENを設定
##LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_ACCESS_TOKEN = "GNJfN3CsYSSuqGBDUrwHqDM6vK5TDXy78kVKMhjaOwKn4MtIcIeKyqhoroLO3dmXE6ZqweGqSRTmZPk+ff1EB3AgxhxFZjsE6E8VE3NTaJDEw0Drtuph2TETjmMHjXbNksROAh4euN7vFC9T/+7tAAdB04t89/1O/w1cDnyilFU="

##環境変数からLINE CHANNEL secretを設定
##LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_CHANNEL_SECRET = "d5bbf1a19949be5f16a4d99b3cabad92"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
@app.route("/callback",methods=['POST'])
def callback():

    #get X-LineSignature header Value
    signature = request.headers['X-Line-Signature']

    #get request bodyas Text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature, please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
    #MessageEvent

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=True)
