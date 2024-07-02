# MusicEventLineBot
This is a linebot where users can search live music events based on given time and location.<br>
音樂演出資訊LineBot -- Tune in Live

## 主要功能
- Live Music: 使用者可選擇日期、地點即可獲得相關的音樂演出資訊
- Keyword: 使用者可輸入關鍵字，返回相關活動資訊
- Fresh Beats: 根據使用者選擇的音樂類型，隨機推薦音樂

## 檔案說明
- requirements.txt > 此app會需要安裝的套件（可在終端機使用 pip freeze > requirements.txt 得到所需套件）
- app.py > 跑的主程式(flask, linebot)
- /backend > DB 查找資料相關函式
- /message_template > LineBot使用的Flex message Json file
- /api > GoogleMapAPI, SpotifyAPI 函式
- /scraping_local > 本機跑的爬蟲程式、以及儲存至Render PostgreSQL

## Deploy Steps
註：正常情況下使用runtime python跑即可，如要在Render使用selenium需使用Docker，但速度太慢故捨棄改用地端跑爬蟲<br>
1. Render > Deploy Web Services > Connect to your Github repo
2. Deploy 設定都留預設即可
3. 複製左上角網址，最後面要加上/callback (e.g. https://xxxx.onrender.com/callback)
4. 到Line Developer > Messaging API > 更改 Webhook URL
5. 只要你的repo有commit change, render會自動 re-deploy

## Render Env Variable
- 建議把較機密的資訊如API Key, DB URL存到Render env varialbe而不是放在code裡
- https://docs.render.com/configure-environment-variables

## LineBot (筆記區）
### 文件
- Line Developer Document 主要是白話的介紹跟json file <br> 
https://developers.line.biz/en/reference/messaging-api/
- Line Python SDK 主要的程式碼，因為python會有固定的命名方式，所以有時json的變數名稱會跟python不同，要以sdk為主<br>
https://github.com/line/line-bot-sdk-python/tree/master

- ChatGPT：看不懂就直接請他解釋 超好用XD

### 簡單說明
以下包含line官方文件跟sdk code本身（可確認參數名字）
- **Event系列**：使用者做的動作（傳訊息、加入離開等）
  <br> 我們主要用到就是Message Event（使用者傳訊息）、Postback event （使用者做postback action，例如：選擇日期時間）<br>
https://developers.line.biz/en/reference/messaging-api/#webhook-event-objects

- **Template系列**：傳訊息line先做好的template，有不同Template可用，Buttons, Confirm等等，再使用TemplateSendMessage送出
https://developers.line.biz/en/reference/messaging-api/#template-messages<br>
https://github.com/line/line-bot-sdk-python/blob/master/linebot/models/template.py#L72

- **Actions系列**：每個template可以搭配不同action使用，比如讓使用者選日期、打開網址等等
https://developers.line.biz/en/reference/messaging-api/#action-objects<br>
https://github.com/line/line-bot-sdk-python/blob/master/linebot/models/actions.py#L180

- **SendMessage系列**：看想要傳給使用者什麼樣的訊息使用，有各種不同LocationSendMessage、AudioSendMessage等等
https://developers.line.biz/en/docs/messaging-api/message-types/#page-title<br>
https://github.com/line/line-bot-sdk-python/blob/master/linebot/models/send_messages.py

### Code解釋
```
@handler.add(MessageEvent, message=Message)
# Flask 處理訊息的路由，這裏為只要是MessageEvent（使用者傳訊息）就走這條路處理，且不限message種類。
# 例如如果是 (MessageEvent, message=StickerMessage) 那只有當使用者傳貼圖的時候，他才會走下面的邏輯判斷。
# Event可以理解是使用者做的動作，像傳訊息MessageEvent,也有JoinEvent等（使用者把帳號加到群組），PostbackEvent（當使用者選取日期時間等等）


def handle_message(event):

    # event.message.text 是取得使用者傳的訊息

    if event.message.text.lower() == "live music":

        # 這裡用的是buttons template，也有不同template可用
        # 設定buttons template裡面的變數，詳細有什麼attribute可設定要參考sdk官方文件
        buttons_template = ButtonsTemplate(
            title='選擇日期',
            text='請選擇',

        # 定義按鈕做的動作，有不同動作可用
        # 為什麼是這樣寫要參考sdk文件
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

        # 這裡是用TemplateSendMessage去傳訊息給使用者（再包buttons)，也可以用其他種SendMessage，每種帶的參數可能不同
        # 有傳貼圖、傳地點等（StickerSendMessage、LocationSendMessage）
        template_message = TemplateSendMessage(
            alt_text='選擇日期和時間',
            template=buttons_template
        )

        # 回覆使用者用的主要的程式碼，event.reply_token是帶token（認證）、第二個變數就是你要回傳的訊息
        # 只可使用一次（例如想要回使用者兩句話，不能複製兩行來使用）
        line_bot_api.reply_message(event.reply_token, template_message)

```
