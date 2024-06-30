from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime


def fetch_tixcraft_data():
    # 設置 ChromeOptions
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=options)
    try:
        # 打開目標網頁
        driver.get('https://tixcraft.com/activity')

        # 等待頁面加載
        time.sleep(5)

        # 點擊成列表式節目資訊
        small = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#display-type > li:nth-child(2)'))
        )
        small.click()

        # 等待頁面更新
        time.sleep(2)

        # 查找所有鏈接
        link_elements = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-outline-primary.text-bold.m-0")

        # 提取所有鏈接的 href 屬性
        links = [link.get_attribute("href") for link in link_elements]
    finally:
        # 關閉瀏覽器
        driver.quit()

    # 將鏈接轉為 DataFrame
    links_df = pd.DataFrame(links, columns=['PageURL'])

    # 設置請求標頭
    header = {'User-Agent': 'William-requests/2.31.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
              'Connection': 'keep-alive'}
    url = 'https://tixcraft.com/activity'

    # 發送 GET 請求
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    # 獲取音樂、演唱會資訊
    tixcraft_info = soup.find_all('div', {'class': 'col-lg-8 col-md-7 col-sm-8 col-xs-5 col-12 mb-2 mb-sm-0'})
    # 獲取圖片資訊
    images = soup.find_all('img', {'class': 'img-fluid'})

    result = []
    image_urls = []

# 定義英文轉中文
    weekday_mapping = {
        'Mon': '一',
        'Tue': '二',
        'Wed': '三',
        'Thu': '四',
        'Fri': '五',
        'Sat': '六',
        'Sun': '日'
    }


    # 瀏覽全部的活動資訊
    for info in tixcraft_info:
        # 時間資訊
        date_div = info.find('div', {'class': 'text-small date'})
        if date_div:
            date = date_div.text.strip()
            try:
                if ' ~ ' in date:
                    start_date_str, end_date_str = date.split(' ~ ')
                    start_date = datetime.strptime(start_date_str.strip(), '%Y/%m/%d (%a.)')
                    end_date = datetime.strptime(end_date_str.strip(), '%Y/%m/%d (%a.)')
                    # 轉換開始日期的星期幾為中文
                    start_weekday_english = start_date.strftime('%a')
                    start_weekday_chinese = weekday_mapping.get(start_weekday_english, start_weekday_english)
                    # 轉換結束日期的星期幾為中文
                    end_weekday_english = end_date.strftime('%a')
                    end_weekday_chinese = weekday_mapping.get(end_weekday_english, end_weekday_english)
                    # 格式化日期
                    formatted_date = (
                        f"{start_date.strftime('%Y/%m/%d')} "
                        f"({start_weekday_chinese}) ~ "
                        f"{end_date.strftime('%Y/%m/%d')} "
                        f"({end_weekday_chinese})"
                    )

                else:
                    original_date_format = datetime.strptime(date, '%Y/%m/%d (%a.)')
                    # 將英文星期幾轉換為中文
                    weekday_english = original_date_format.strftime('%a')
                    weekday_chinese = weekday_mapping.get(weekday_english, weekday_english)
                    formatted_date = original_date_format.strftime(f'%Y/%m/%d ({weekday_chinese})')
            except ValueError:
                formatted_date = "日期格式錯誤"
        else:
            formatted_date = "無日期信息"
        # 活動名稱
        titles_div = info.find('div', {'class': 'text-bold pt-1 pb-1'})
        titles = titles_div.text.strip() if titles_div else "無活動名稱"

        # 活動地點
        location_div = info.find('div', {'class': 'text-small text-med-light'})
        location = location_div.text.strip() if location_div else "無活動地點"
        result.append((titles, formatted_date, location))

    # 獲取圖片網址
    for img in images:
        img_url = img.get('src')
        if img_url:
            image_urls.append(img_url)

    # 用成 DataFrame 格式
    activity_df = pd.DataFrame(result, columns=['EventName', 'EventTime', 'Venue'])
    # 插入「圖片網址」欄位
    image_urls = image_urls[:len(activity_df)]
    activity_df['ImageURL'] = image_urls
    # 將activity_df, links_df結合成一個df
    df = pd.concat([activity_df, links_df], axis=1)

    return df

