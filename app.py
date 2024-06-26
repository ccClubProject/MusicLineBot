import sqlite3
import os
import re
import urllib.parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import json

# 引入backend資料庫相關自訂模組
from backend.build import *

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 使用backend模組，將爬蟲資料存進table
create_table()

selected_date = None  # 全局變數來儲存選擇的日期

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=Message)
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
        handle_location_message(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    global selected_date
    data = event.postback.data
    if 'action=sel_date' in data:
        selected_date = event.postback.params['date']
        response_text = f"您選擇的日期是：{selected_date}"
    elif 'action=no_date' in data:
        selected_date = None
        response_text = "不指定"
    else:
        response_text = "未知的動作"
    
    buttons_template = ButtonsTemplate(
        title='想找哪個地區呢？',
        text='請選擇地區',
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
                label='東部及離島',
                text='東部及離島'
            )
        ]
    )
    
    template_message = TemplateSendMessage(
        alt_text='選擇地區',
        template=buttons_template
    )

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=response_text),
            template_message
        ]
    )

    if 'date=' in data:
        location, date = data.split('&date=')
        events = get_random_music_events(date, location)
        if events:
            events_text = '\n'.join([f"活動開始時間: {event[0]}, 活動結束時間: {event[1]}, 地址: {event[2]}" for event in events])
        else:
            events_text = "沒有找到符合的活動。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=events_text))

def handle_location_message(event):
    global selected_date
    message = event.message.text

    if re.match('北部', message):
        flex_message = TextSendMessage(text='你在北部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(label="台北市", text="台北市", data=f'台北市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="新北市", text="新北市", data=f'新北市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="基隆市", text="基隆市", data=f'基隆市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="桃園市", text="桃園市", data=f'桃園市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="新竹市", text="新竹市", data=f'新竹市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="新竹縣", text="新竹縣", data=f'新竹縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="宜蘭縣", text="宜蘭縣", data=f'宜蘭縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('中部', message):
        flex_message = TextSendMessage(text='你在中部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(label="苗栗縣", text="苗栗縣", data=f'苗栗縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="台中市", text="台中市", data=f'台中市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="彰化縣", text="彰化縣", data=f'彰化縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="南投縣", text="南投縣", data=f'南投縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="雲林縣", text="雲林縣", data=f'雲林縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('南部', message):
        flex_message = TextSendMessage(text='你在南部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(label="高雄市", text="高雄市", data=f'高雄市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="台南市", text="台南市", data=f'台南市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="嘉義市", text="嘉義市", data=f'嘉義市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="嘉義縣", text="嘉義縣", data=f'嘉義縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="屏東縣", text="屏東縣", data=f'屏東縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('東部及離島', message):
        flex_message = TextSendMessage(text='你在東部及離島的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(label="花蓮縣", text="花蓮縣", data=f'花蓮縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="台東縣", text="台東縣", data=f'台東縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="澎湖縣", text="澎湖縣", data=f'澎湖縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="金門縣", text="金門縣", data=f'金門縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackAction(label="連江縣", text="連江縣", data=f'連江縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        # 對於其他消息簡單回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)