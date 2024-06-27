import sqlite3
import os
import re
import urllib.parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
# from search_tracks import *
import json

# 引入backend資料庫相關自訂模組
from backend.query_db import *

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


selected_date = None

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

#測試套用template的日期選單

from music_event_template import buttons_template

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global selected_date
    input_message = event.message.text
    if input_message.lower() == "live music":

        template_message = TemplateSendMessage(
            alt_text='選擇日期和時間',
            template = buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global selected_date
    input_message = event.message.text
    if input_message.lower() == "live music":
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
'''
    # 關鍵字搜尋（連至DB query活動名稱欄位)
    elif re.match('找', input_message):
        keyword = input_message.replace("找", "").strip()
        search_result = search_events(keyword)
        if len(search_result) != 2:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=search_result))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無此活動！換個關鍵字吧！'))
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
        response_text = "不指定日期"
    elif 'date=' in data:
        location, date = data.split('&date=')
        response_text = f"您選擇的日期和地點是：{location},{date}"
    else:
        response_text = "未知的動作"

    if 'action=sel_date' in data or 'action=no_date' in data:
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
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_text)
        )

def handle_location_message(event):
    global selected_date
    message = event.message.text
    if re.match('北部', message):
        flex_message = TextSendMessage(text='你在北部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="台北市", data=f'台北市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新北市", data=f'新北市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="基隆市", data=f'基隆市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="桃園市", data=f'桃園市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新竹市", data=f'新竹市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="新竹縣", data=f'新竹縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="宜蘭縣", data=f'宜蘭縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('中部', message):
        flex_message = TextSendMessage(text='你在中部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="苗栗縣", data=f'苗栗縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台中市", data=f'台中市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="彰化縣", data=f'彰化縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="南投縣", data=f'南投縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="雲林縣", data=f'雲林縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('南部', message):
        flex_message = TextSendMessage(text='你在南部的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="高雄市", data=f'高雄市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台南市", data=f'台南市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="嘉義市", data=f'嘉義市&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="嘉義縣", data=f'嘉義縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="屏東縣", data=f'屏東縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('東部及離島', message):
        flex_message = TextSendMessage(text='你在東部及離島的哪個縣市呢？',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackTemplateAction(label="花蓮縣", data=f'花蓮縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="台東縣", data=f'台東縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="澎湖縣", data=f'澎湖縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="金門縣", data=f'金門縣&date={selected_date}')),
                                           QuickReplyButton(action=PostbackTemplateAction(label="連江縣", data=f'連江縣&date={selected_date}'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

'''
以下是嘗試跟Music_event_template串接
待處理:
*要等選完日期地點，進到DB抓完資料，回傳串列後執行判斷

#推薦展演活動，回傳Bubbles
@handler.add(MessageEvent, message=TextMessage)
def handle_recommend_event(event):
    message = event.message.text
    if *要等選完日期地點，進到DB抓完資料，回傳串列後執行判斷
        message = event_carousel('推薦展演結果', image_url_table, event_name_table, date_table, location_table, page_url_table, google_url_table)
        line_bot_api.reply_message(event.reply_token, message)

#當展演活動大於10個，需要推薦更多
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data.startswith('show_more'):
        _, start_index = data.split(',')
        start_index = int(start_index)
        message = event_carousel('推薦展演結果', image_url_table, event_name_table, date_table, location_table, page_url_table, google_url_table, start_index=start_index)
        line_bot_api.reply_message(event.reply_token, message)
'''



''' 來點新鮮的
@handler.add(MessageEvent, message=TextMessage)
def music(event):
    if event.message.text == "來點新鮮的":
        carousel_template = TemplateSendMessage(
            alt_text='請選擇音樂類型',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='流行音樂',
                        text='點選以收聽流行音樂',
                        actions=[MessageAction(label='流行音樂', text='流行音樂')]
                    ),
                    CarouselColumn(
                        title='搖滾音樂',
                        text='點選以收聽搖滾音樂',
                        actions=[MessageAction(label='搖滾音樂', text='搖滾音樂')]
                    ),
                    CarouselColumn(
                        title='嘻哈音樂',
                        text='點選以收聽嘻哈音樂',
                        actions=[MessageAction(label='嘻哈音樂', text='嘻哈音樂')]
                    ),
                    CarouselColumn(
                        title='電子音樂',
                        text='點選以收聽電子音樂',
                        actions=[MessageAction(label='電子音樂', text='電子音樂')]
                    ),
                    CarouselColumn(
                        title='爵士音樂',
                        text='點選以收聽爵士音樂',
                        actions=[MessageAction(label='爵士音樂', text='爵士音樂')]
                    ),
                    CarouselColumn(
                        title='古典音樂',
                        text='點選以收聽古典音樂',
                        actions=[MessageAction(label='古典音樂', text='古典音樂')]
                    ),
                    CarouselColumn(
                        title='R&B和靈魂音樂',
                        text='點選以收聽R&B和靈魂音樂',
                        actions=[MessageAction(label='R&B和靈魂音樂', text='R&B和靈魂音樂')]
                    ),
                    CarouselColumn(
                        title='鄉村音樂',
                        text='點選以收聽鄉村音樂',
                        actions=[MessageAction(label='鄉村音樂', text='鄉村音樂')]
                    ),
                    CarouselColumn(
                        title='隨機推薦',
                        text='點選以獲得隨機推薦',
                        actions=[MessageAction(label='隨機推薦', text='隨機推薦')]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template)
    elif event.message.text in ['流行音樂', '搖滾音樂', '嘻哈音樂', '電子音樂', '爵士音樂', '古典音樂', 'R&B和靈魂音樂', '鄉村音樂']:
        token = get_token()
        # 輸出為字典格式
        track = search_tracks_by_genre(event.message.text, token)
        if track:
            # 曲目資訊
            columns = []
            columns.append(CarouselColumn(thumbnail_image_url=track['image_url'], title=track['title'], text=track['artist'], actions=[URIAction(label='詳細資訊', uri=track['details_url'])]))
            carousel_template = TemplateSendMessage(alt_text='選擇曲目', template=CarouselTemplate(columns=columns))
            line_bot_api.reply_message(event.reply_token, carousel_template)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，找不到相關曲目。")
            )
    elif event.message.text == '隨機推薦':
        token = get_token()
        track = random_recommendations(token)
        if track:
            # 曲目資訊
            columns = []
            columns.append(
                CarouselColumn(thumbnail_image_url=track['image_url'], title=track['title'], text=track['artist'],
                               actions=[URIAction(label='詳細資訊', uri=track['details_url'])]))
            carousel_template = TemplateSendMessage(alt_text='選擇曲目', template=CarouselTemplate(columns=columns))
            line_bot_api.reply_message(event.reply_token, carousel_template)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，我不太了解你的需求。")
        )
'''

# 當py檔案被直接執行時，__name__變數會是__main__，因此當此條件成立時，代表程式被當作主程式執行，而不是被當作模組引用。
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    app.run()
