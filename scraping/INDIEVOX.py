import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime

# 初始化 WebDriver
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)
driver.maximize_window()

def get_event_data(url):
    driver.get(url)
    driver.implicitly_wait(5)

    # 捲動頁面以加載更多內容
    for i in range(30):
        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        time.sleep(2)

    # 提取活動元素
    event_elements = driver.find_elements(By.CSS_SELECTOR, '#activityListTab tr')

    # 提取活動信息
    event_data = []
    for event in event_elements:
        details = event.find_elements(By.TAG_NAME, 'td')
        if len(details) >= 3:
            # 活動日期
            date = details[0].text
            # 活動名稱
            name = details[1].text
            # 活動地點
            location = details[2].text
            event_data.append((date, name, location))

    # 創建 DataFrame
    df = pd.DataFrame(event_data, columns=['EventTime', 'EventName', 'Venue'])
    return df

def get_combined_event_data(url_table, url_card):
    # 獲取資料
    df_table = get_event_data(url_table)
    df_card = get_event_data(url_card)

    # 關閉瀏覽器
    driver.quit()

    # 合併兩個 DataFrame
    df_combined = pd.concat([df_table, df_card], ignore_index=True)
    return df_combined

# 指定網址
url_table = 'https://www.indievox.com/activity/list?type=table&startDate=2024%2F06%2F13&endDate='
url_card = 'https://www.indievox.com/activity/list?type=card&startDate=2024%2F06%2F14&endDate='

df_combined = get_combined_event_data(url_table, url_card)

# 顯示 DataFrame
print(df_combined.to_string())
