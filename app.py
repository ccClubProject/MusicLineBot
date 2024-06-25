#flex message JSON檔
def create_bubble(event):
    bubble_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": event[6],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3.5",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": event[1],
                                    "size": "xl",
                                    "color": "#ffffff",
                                    "weight": "bold"
                                }
                            ],
                            "spacing": "none"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": event[8],
                                    "color": "#ebebeb",
                                    "size": "md",
                                    "flex": 0
                                }
                            ],
                            "spacing": "none",
                            "margin": "xs"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": event[3],
                                    "color": "#ffffff",
                                    "weight": "regular"
                                }
                            ],
                            "spacing": "none",
                            "margin": "xs"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://i.imgur.com/McOT6MH.png",
                                            "margin": "none"
                                        },
                                        {
                                            "type": "text",
                                            "text": "購票去",
                                            "color": "#ffffff",
                                            "flex": 0,
                                            "offsetTop": "-2px",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "spacing": "sm"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "borderWidth": "1px",
                            "cornerRadius": "4px",
                            "spacing": "md",
                            "borderColor": "#ffffff",
                            "margin": "xl",
                            "height": "40px",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": event[7]
                            }
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://i.imgur.com/QAg1q20.png"
                                        },
                                        {
                                            "type": "text",
                                            "text": "展演地點",
                                            "color": "#ffffff",
                                            ""flex": 0,
                        "offsetTop": "-2px",
                        "margin": "sm"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "md",
                "borderColor": "#ffffff",
                "margin": "lg",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": "https://maps.app.goo.gl/Ney2hjkBrUsjLqdV7"
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#3D3D3Dcc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          }
        ],
        "paddingAll": "0px"
      },
      "size": "kilo"
    }

    return bubble_template

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
        handle_location_message(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=sel_date' in data:
        selected_date = event.postback.params['date']
        response_text = f"您選擇的日期是：{selected_date}"
        state = 'date_selected'
    elif 'action=no_date' in data:
        selected_date = None
        response_text = "不指定日期"
        state = 'date_not_selected'
    else:
        response_text = "未知的動作"
        state = None
    
    if state == 'date_selected':
        buttons_template = ButtonsTemplate(
            title='想找哪個地區呢？',
            text='請選擇地區',
            actions=[
                MessageAction(
                    label='北部',
                    text=f'北部&{selected_date}'
                ),
                MessageAction(
                    label='中部',
                    text=f'中部&{selected_date}'
                ),
                MessageAction(
                    label='南部',
                    text=f'南部&{selected_date}'
                ),
                MessageAction(
                    label='東部及離島',
                    text=f'東部及離島&{selected_date}'
                )
            ]
        )
    else:
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

    # 合併兩個回覆為一個
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=response_text),
            template_message
        ]
    )

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
        flex_message = TextSendMessage(text='你在東部&離島的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="花蓮縣", text="花蓮縣", data='B&花蓮縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台東縣", text="台東縣", data='B&台東縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="澎湖縣", text="澎湖縣", data='B&澎湖縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="金門縣", text="金門縣", data='B&金門縣')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="連江縣", text="連江縣", data='B&連江縣'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

    #從資料庫推薦符合日期和地點的活動
    elif '&' in message:
        location, date = message.split('&')
        music_events = get_random_music_events(date, location)
        if music_events:
            bubbles = []
            for event in music_events:
                bubble = create_bubble(event)
                bubbles.append(bubble)
            flex_message = FlexSendMessage(
                alt_text='推薦的音樂表演',
                contents={
                    'type': 'carousel',
                    'contents': bubbles
                }
            )
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="'查無此活動！換個日期地點吧！"))


    # 新版關鍵字搜尋（進DB query活動名稱欄位)
    elif re.match('找', message):
        keyword = message.replace("找", "").strip()
        search_result = get_data(keyword)
        if len(search_result) != 2:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=search_result))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無此活動！換個關鍵字吧！'))
    else:
        # 對於其他消息簡單回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))




# 當py檔案被直接執行時，__name__變數會是__main__，因此當此條件成立時，代表程式被當作主程式執行，而不是被當作模組引用。
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)