from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

#line_bot_api = 'oTDLJU6SuW1G1t1H9xyp1ZNiD3KbZ8RjR089SsBI2AcKmr8YMHUZQR1OF+h5xQnoHRBt0t5Li6/i6CL1V2Kq9DfWzy1zmE0Lf1Wi59CxxiANJA6C24bWd4cxt1kNr6VQZ1a2opNlfRH5laUdAaBW7QdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
#handler = WebhookHandler('745df55dba827e8148615aabfaeca14d')
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)