import sqlite3
import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.models import (
    MessageEvent, TextMessage as LineTextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, DatetimePickerTemplateAction, PostbackEvent, PostbackTemplateAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)
line_bot_api = MessagingApi(api_client=ApiClient(configuration=configuration))

# 所有從line來的事件都會先經過此，再轉為下方的handler做進一步的處理
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=LineTextMessage)
def handle_message(event):
    if event.message.text.lower() == "live music":
        buttons_template = ButtonsTemplate(
            title='選擇日期和時間',
            text='請選擇',
            actions=[
                DatetimePickerTemplateAction(
                    label='選擇日期',
                    data='action=sel_date',
                    mode='date'
                ),
                DatetimePickerTemplateAction(
                    label='選擇時間',
                    data='action=sel_time',
                    mode='time'
                ),
                DatetimePickerTemplateAction(
                    label='選擇日期和時間',
                    data='action=sel_datetime',
                    mode='datetime'
                ),
                PostbackTemplateAction(
                    label='不指定',
                    data='action=no_date'
                )
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='選擇日期和時間',
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=sel_date' in data:
        response_text = f"您選擇的日期是：{event.postback.params['date']}"
    elif 'action=sel_time' in data:
        response_text = f"您選擇的時間是：{event.postback.params['time']}"
    elif 'action=sel_datetime' in data:
        response_text = f"您選擇的日期和時間是：{event.postback.params['datetime']}"
    elif 'action=no_date' in data:
        response_text = "您選擇了不指定日期"
    else:
        response_text = "未知的動作"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text)
    )

if __name__ == "__main__":
    app.run(debug=True)

    