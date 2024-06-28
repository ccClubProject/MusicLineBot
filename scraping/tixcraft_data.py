from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


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
    links_df = pd.DataFrame(links, columns=['售票網址'])

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

    # 瀏覽全部的活動資訊
    for info in tixcraft_info:
        # 時間資訊
        date = info.find('div', {'class': 'text-small date'}).text
        # 活動名稱
        titles = info.find('div', {'class': 'text-bold pt-1 pb-1'}).text
        # 活動地點
        location = info.find('div', {'class': 'text-small text-med-light'}).text
        result.append((date, titles, location))

    # 獲取圖片網址
    for img in images:
        img_url = img.get('src')
        if img_url:
            image_urls.append(img_url)

    # 用成 DataFrame 格式
    activity_df = pd.DataFrame(result, columns=['活動日期', '活動名稱', '地點'])
    # 插入「圖片網址」欄位
    image_urls = image_urls[:len(activity_df)]
    activity_df['圖片網址'] = image_urls
    # 將activity_df, links_df結合成一個df
    df = pd.concat([activity_df, links_df], axis=1)

    return df


# 使用範例
if __name__ == "__main__":
    df = fetch_tixcraft_data()
    df.to_excel('拓元售票資料', index=False)
    # print(df.to_string())

