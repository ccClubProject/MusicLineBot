import os
import re
import urllib.parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, DatetimePickerTemplateAction, PostbackEvent,
    PostbackTemplateAction, MessageAction, QuickReply, QuickReplyButton,URIAction
)

app = Flask(__name__)
channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
        response_text = f"您選擇的日期是：{event.postback.params['date']}"
    elif 'action=no_date' in data:
        response_text = "不指定"
    else:
        response_text = "未知的動作"

    # 準備回覆的訊息，包括選擇日期的回覆和地區選擇按鈕
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
                label='東部&離島',
                text='東部&離島'
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

    #關鍵字搜尋
    elif re.match('找', message):
        search = message.replace("找", "").strip()
        search_word = search.encode("utf-8")
        search_url_indievox = f"https://www.indievox.com/activity/list/{urllib.parse.quote(search_word)}"
        search_url_kktix = f"https://kktix.com/events?utf8=%E2%9C%93&search={urllib.parse.quote(search_word)}&start_at=2024%2F06%2F22"
        search_url_accupass = f"https://www.accupass.com/search?q={urllib.parse.quote(search_word)}"
        search_url_tixcraft = f"https://tixcraft.com/activity/{urllib.parse.quote(search_word)}"
        confirm_message = TemplateSendMessage(
            alt_text='點擊連結前往搜尋結果',
            template=ButtonsTemplate(
                title=f"{search}搜尋結果出爐！",
                text=f"點擊按鈕看{search}有哪些好活動",
                actions=[
                    URIAction(
                        label='馬上前往iNDEIVOX',
                        uri=search_url_indievox),
                    URIAction(
                        label='馬上前往kktix',
                        uri=search_url_kktix),
                    URIAction(
                        label='馬上前往Accupass',
                        uri=search_url_accupass),
                    URIAction(
                        label='馬上前往Tixcraft',
                        uri=search_url_tixcraft)
                ]))
        line_bot_api.reply_message(event.reply_token, confirm_message)

    else:
        # 對於其他消息簡單回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    app.run(debug=True)


