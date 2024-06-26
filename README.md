# MusicEventLineBot
This is a linebot where users can search live music events based on given time and location.

## 官方文件
https://docs.render.com/deploy-flask

## 檔案說明
- requirements.txt > 此app會需要安裝的套件（可在終端機使用 pip freeze > requirements.txt 得到所需套件）
- app.py > 跑的主程式(flask, linebot)
- backend/build.py > 建立DB及查找資料相關函式
- backend/init.sql > 定義DB schema
- backend/scraped.db > DB本身（存取爬蟲資料）
- scraping/accupass.py > accupass爬蟲程式

## Deploy Steps (正常情況下使用python跑即可)
1. Render > Deploy Web Services > Connect to your Github repo
2. Deploy 設定都留預設即可
3. 複製左上角網址，最後面要加上/callback (e.g. https://xxxx.onrender.com/callback)
4. 到Line Developer > Messaging API > 更改 Webhook URL
5. 只要你的repo有commit change, render會自動 re-deploy<br>

<b>因為有使用selenium，所以Language使用docker deploy，會需要dockerfile去建置所需環境（如：安裝chrome driver)</b>

## Render Env Variable
- 建議把較機密的資訊如API Key, DB URL存到Render env varialbe而不是放在code裡
- https://docs.render.com/configure-environment-variables

## LineBot

```
# 處理訊息的路由，這裏為只要是MessageEvent（使用者傳訊息）就走這條路處理，且不限message種類。
# 例如如果是 (MessageEvent, message=StickerMessage) 那只有當使用者傳貼圖的時候，他才會走下面的邏輯判斷。
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

```
