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

## Deploy Steps(正常情況下使用web services即可)
1. Render > Deploy Web Services > Connect to your Github repo
2. Deploy 設定都留預設即可
3. 複製左上角網址，最後面要加上/callback (e.g. https://xxxx.onrender.com/callback)
4. 到Line Developer > Messaging API > 更改 Webhook URL
5. 只要你的repo有commit change, render會自動 re-deploy
<b>因為有使用selenium，所以用docker deploy，會需要dockerfile去建置所需環境（如：安裝chrome driver)</b>

## Render Env Variable
- 建議把較機密的資訊如API Key, DB URL存到Render env varialbe而不是放在code裡
- https://docs.render.com/configure-environment-variables
