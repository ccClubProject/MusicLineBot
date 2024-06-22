import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, DatetimePickerTemplateAction, PostbackEvent, PostbackTemplateAction,
    MessageAction, QuickReply, QuickReplyButton
)
import re

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == "live music":
        buttons_template = ButtonsTemplate(
            title='選擇日期',
            text='請選擇',
            actions=[
                DatetimePickerTemplateAction(
                    label='選擇日期',
                    data='action=sel_date',
                    mode='date'
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
    elif 'action=no_date' in data:
        response_text = "不指定"
    else:
        response_text = "未知的動作"

    # 回覆日期
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text)
    )

    # 詢問地理位置
    buttons_template = ButtonsTemplate(
        title='想找哪個地區呢？',
        text='暫不支援離島地區',
        actions=[
            MessageAction(
                label='北部',
                text='北部'
            ),
            MessageAction(
                label='中部',
                text='中部'
            ),
            MessageAction(
                label='南部',
                text='南部'
            ),
            MessageAction(
                label='東部',
                text='東部'
            )
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='選擇地區',
        template=buttons_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_location_message(event):
    message = event.message.text
    if re.match('北部', message):
        flex_message = TextSendMessage(text='你在北部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="台北市", text="台北市", data='B&台北市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新北市", text="新北市", data='B&新北市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="基隆市", text="基隆市", data='B&基隆市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="桃園市", text="桃園市", data='B&桃園市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新竹市", text="新竹市", data='B&新竹市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新竹縣", text="新竹縣", data='B&新竹縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="宜蘭縣", text="宜蘭縣", data='B&宜蘭縣'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('中部', message):
        flex_message = TextSendMessage(text='你在中部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="苗栗縣", text="苗栗縣", data='B&苗栗縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台中市", text="台中市", data='B&台中市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="彰化縣", text="彰化縣", data='B&彰化縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="南投縣", text="南投縣", data='B&南投縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="雲林縣", text="雲林縣", data='B&雲林縣'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('南部', message):
        flex_message = TextSendMessage(text='你在南部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="高雄市", text="高雄市", data='B&高雄市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台南市", text="台南市", data='B&台南市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="嘉義市", text="嘉義市", data='B&嘉義市')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="嘉義縣", text="嘉義縣", data='B&嘉義縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="屏東縣", text="屏東縣", data='B&屏東縣'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('東部', message):
        flex_message = TextSendMessage(text='你在東部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="花蓮縣", text="花蓮縣", data='B&花蓮縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台東縣", text="台東縣", data='B&台東縣'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

if __name__ == "__main__":
    app.run(debug=True)

