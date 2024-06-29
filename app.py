
import sqlite3
import os
import re
import urllib.parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from search_tracks import *
import json

# 引入backend資料庫相關自訂模組
from backend.query_db import *

# 引入template自訂模組
from message_template.picktime_bubble import time_bubble
from message_template.choose_location_bubble import location_bubble
from message_template.event_bubbles import event_carousel

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#關鍵字搜尋(預設關閉)
accepting_keyword_input = False
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global selected_date
    global accepting_keyword_input
    input_message = event.message.text
    #選日期
    if input_message.lower() == "live music":
        flex_message = FlexSendMessage(
            alt_text = "選擇日期",
            contents = time_bubble
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    # 關鍵字搜尋（連至DB query活動名稱欄位)
    elif re.match(r'^我想找', input_message):
        accepting_keyword_input = True
        reply_message = TextSendMessage(text="請輸入您想找的關鍵字")
        line_bot_api.reply_message(event.reply_token, reply_message)
    
    elif accepting_keyword_input:
        keyword = input_message
        accepting_keyword_input = False  # Reset flag after processing

        search_all_info = info_search_by_name(keyword)
        if not search_all_info:
            reply_message = TextSendMessage(text="查無此活動！重新點選表單換個關鍵字吧！")
            line_bot_api.reply_message(event.reply_token, reply_message)
            return

        image_url_table = [info['ImageURL'] for info in search_all_info]
        event_name_table = [info['EventName'] for info in search_all_info]
        date_table = [info['EventTime'] for info in search_all_info]
        location_table = [info['Venue'] for info in search_all_info]
        page_url_table = [info['PageURL'] for info in search_all_info]
        google_url_table = [f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(info['Address'])}" for info in search_all_info]

        flex_message = event_carousel(
            alt_text="推薦展演活動",
            image_url_table=image_url_table,
            event_name_table=event_name_table,
            date_table=date_table,
            location_table=location_table,
            page_url_table=page_url_table,
            google_url_table=google_url_table
        )
        line_bot_api.reply_message(event.reply_token, flex_message)


    # 來點新鮮的
    elif event.message.text == "來點新鮮的":
        carousel_template = TemplateSendMessage(
            alt_text='請選擇音樂類型',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='流行音樂',
                        text='點選以收聽流行音樂',
                        actions=[MessageAction(label='流行音樂', text='Pop')]
                    ),
                    CarouselColumn(
                        title='搖滾音樂',
                        text='點選以收聽搖滾音樂',
                        actions=[MessageAction(label='搖滾音樂', text='Rock')]
                    ),
                    CarouselColumn(
                        title='嘻哈音樂',
                        text='點選以收聽嘻哈音樂',
                        actions=[MessageAction(label='嘻哈音樂', text='Hip Hop/Rap')]
                    ),
                    CarouselColumn(
                        title='電子音樂',
                        text='點選以收聽電子音樂',
                        actions=[MessageAction(label='電子音樂', text='Electronic/Dance')]
                    ),
                    CarouselColumn(
                        title='爵士音樂',
                        text='點選以收聽爵士音樂',
                        actions=[MessageAction(label='爵士音樂', text='Jazz')]
                    ),
                    CarouselColumn(
                        title='古典音樂',
                        text='點選以收聽古典音樂',
                        actions=[MessageAction(label='古典音樂', text='Classical')]
                    ),
                    CarouselColumn(
                        title='R&B和靈魂音樂',
                        text='點選以收聽R&B和靈魂音樂',
                        actions=[MessageAction(label='R&B和靈魂音樂', text='R&B/Soul')]
                    ),
                    CarouselColumn(
                        title='鄉村音樂',
                        text='點選以收聽鄉村音樂',
                        actions=[MessageAction(label='鄉村音樂', text='Country')]
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
    elif event.message.text in ['Pop', 'Rock', 'Hip Hop/Rap', 'Electronic/Dance', 'Jazz', 'Classical', 'R&B/Soul', 'Country']:
        token = get_token()
        # 輸出為字典格式
        track = search_tracks_by_genre(event.message.text, token)
        if track:
            # 曲目資訊列表
            columns = [
                CarouselColumn(
                    thumbnail_image_url=track['image_url'],
                    title=track['title'],
                    text=track['artist'],
                    actions=[
                        URIAction(
                            label='詳細資訊',
                            uri=track['details_url'])])]
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
            # 曲目資訊列表
            columns = [
                CarouselColumn(
                    thumbnail_image_url=track['image_url'],
                    title=track['title'],
                    text=track['artist'],
                    actions=[
                        URIAction(
                            label='詳細資訊',
                            uri=track['details_url'])])]
            carousel_template = TemplateSendMessage(alt_text='選擇曲目', template=CarouselTemplate(columns=columns))
            line_bot_api.reply_message(event.reply_token, carousel_template)

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
    
    #輸入地點日期後從DB推薦活動
    elif 'date=' in data:
        city, time = data.split('&date=')
        if time == "None":
            time = None
        else: time = time
        
        search_all_info = info_search_by_time_city(time, city)
        if not search_all_info:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有找到相關的展演活動，試試其他日期或地點吧!"))
            return

        image_url_table = [info['ImageURL'] for info in search_all_info]
        event_name_table = [info['EventName'] for info in search_all_info]
        date_table = [info['EventTime'] for info in search_all_info]
        location_table = [info['Venue'] for info in search_all_info]
        page_url_table = [info['PageURL'] for info in search_all_info]
        google_url_table = [f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(info['Address'])}" for info in search_all_info]

        flex_message = event_carousel(
            alt_text="推薦展演活動",
            image_url_table=image_url_table,
            event_name_table=event_name_table,
            date_table=date_table,
            location_table=location_table,
            page_url_table=page_url_table,
            google_url_table=google_url_table
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    # 顯示更多活動
    elif data.startswith('show_more,'):
        start_index = int(data.split(',')[1])
        
        # Continue showing events from the last displayed index
        flex_message = event_carousel(
            alt_text="推薦展演活動",
            image_url_table=image_url_table[start_index:],
            event_name_table=event_name_table[start_index:],
            date_table=date_table[start_index:],
            location_table=location_table[start_index:],
            page_url_table=page_url_table[start_index:],
            google_url_table=google_url_table[start_index:],
            start_index=start_index  # Start from the last displayed index
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    else:
        response_text = "未知的動作"


    if 'action=sel_date' in data or 'action=no_date' in data:
        flex_message = FlexSendMessage(
            alt_text = "選擇地區",
            contents = location_bubble
        )
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=response_text),
                flex_message
            ]
        )
    # else:
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=response_text)
    #     )

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
    elif re.match('東部', message):
        flex_message = TextSendMessage(text='你在東部&離島的哪個縣市呢？',
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


'''
#來點新鮮的
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
                        actions=[MessageAction(label='流行音樂', text='Pop')]
                    ),
                    CarouselColumn(
                        title='搖滾音樂',
                        text='點選以收聽搖滾音樂',
                        actions=[MessageAction(label='搖滾音樂', text='Rock')]
                    ),
                    CarouselColumn(
                        title='嘻哈音樂',
                        text='點選以收聽嘻哈音樂',
                        actions=[MessageAction(label='嘻哈音樂', text='Hip Hop/Rap')]
                    ),
                    CarouselColumn(
                        title='電子音樂',
                        text='點選以收聽電子音樂',
                        actions=[MessageAction(label='電子音樂', text='Electronic/Dance')]
                    ),
                    CarouselColumn(
                        title='爵士音樂',
                        text='點選以收聽爵士音樂',
                        actions=[MessageAction(label='爵士音樂', text='Jazz')]
                    ),
                    CarouselColumn(
                        title='古典音樂',
                        text='點選以收聽古典音樂',
                        actions=[MessageAction(label='古典音樂', text='Classical')]
                    ),
                    CarouselColumn(
                        title='R&B和靈魂音樂',
                        text='點選以收聽R&B和靈魂音樂',
                        actions=[MessageAction(label='R&B和靈魂音樂', text='R&B/Soul')]
                    ),
                    CarouselColumn(
                        title='鄉村音樂',
                        text='點選以收聽鄉村音樂',
                        actions=[MessageAction(label='鄉村音樂', text='Country')]
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
    elif event.message.text in ['Pop', 'Rock', 'Hip Hop/Rap', 'Electronic/Dance', 'Jazz', 'Classical', 'R&B/Soul', 'Country']:
        token = get_token()
        # 輸出為字典格式
        track = search_tracks_by_genre(event.message.text, token)
        if track:
            # 曲目資訊列表
            columns = [
                CarouselColumn(
                    thumbnail_image_url=track['image_url'],
                    title=track['title'],
                    text=track['artist'],
                    actions=[
                        URIAction(
                            label='詳細資訊',
                            uri=track['details_url'])])]
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
            # 曲目資訊列表
            columns = [
                CarouselColumn(
                    thumbnail_image_url=track['image_url'],
                    title=track['title'],
                    text=track['artist'],
                    actions=[
                        URIAction(
                            label='詳細資訊',
                            uri=track['details_url'])])]
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
