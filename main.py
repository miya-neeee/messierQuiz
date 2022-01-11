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
    FollowEvent, MessageEvent, TextMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonTemplate, PostbakTemplateAction, MessageTemplateAction, URITemplateAction
)
import os

##WebApplicationFlamework:flask
app = Flask(_name_)

##環境変数からLINE ACCESS TOKENを設定
LINE_CHANNEL_ACCEASS_TOKEN = os.environ["LINE_CHANNEL_ACCEASS_TOKEN"]
##環境変数からLINE CHANNEL secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCEASS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
@app.route("/callback",methods=['POST'])
def callback():

    #get X-LineSignature header Value
    signature = request.headers['X-Line-Signature']

    #get request bodyas Text
    body = request.get_data(as_text=True)
    app.loger.info("Request body: " + body)
    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
        return 'OK'
    #MessageEvent
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        if event.reply_token == "00000000000000000000000000000000":
            return

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    if __name__=="__main__":
        port = int(os.getenv("PORT"))
        app.run(host="0.0.0.0", port=port)
