import requests
from dotenv import load_dotenv  # 用於讀取.env文件中的環境變量
import os  # 用於訪問操作系統的環境變量
import webbrowser

# 加載 .env 文件中的環境變量
load_dotenv()
# 從環境變量中讀取API密鑰
google_map_api = os.getenv("GOOGLE_MAP_API")

# 展演空間的「地址」
def formatted__address(show_loc):
    # 「尋找地點」的url
    find_place_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {"key": google_map_api,
              "input": show_loc,
              "inputtype": "textquery",
              "language": "zh-TW",
              "fields": "formatted_address,geometry"
              }
    # 發送請求並獲取回應
    response = requests.get(find_place_url, params=params)
    data = response.json()
    if data['candidates']:
        address = data['candidates'][0]['formatted_address']
        return address
    else:
        return None

# 展演空間的「經緯度」
def lng_lat(show_loc):
    # 「尋找地點」的url
    find_place_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    # 請求內容
    params = {"key": google_map_api,
              "input": show_loc,
              "inputtype": "textquery",
              "language": "zh-TW",
              "fields": "formatted_address,geometry"
              }
    # 發送請求並獲取回應
    response = requests.get(find_place_url, params=params)
    data = response.json()
    if data['candidates']:
        location = data['candidates'][0]['geometry']['location']
        return location
    else:
        return None

# 使用者裝置當下位置
def current_loc():
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + google_map_api
    data = {"considerIp": "true"}
    response = requests.post(url, json=data)
    location = response.json().get('location')
    if location:
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None

# 導航
def route_planning():
    # 獲取用戶輸入
    show_loc = input("請輸入展演空間名稱:")
    # 獲取展演空間地址和位置
    address = formatted__address(show_loc)
    dest_location = lng_lat(show_loc)
    if not address:
        return "無法找到展演空間，請檢查名稱是否正確。"

    # 獲取當前位置
    origin_lat, origin_lng = current_loc()
    if not origin_lat or not origin_lng:
        return "無法獲取當前位置。"

    origin = f"{origin_lat},{origin_lng}"
    destination = f"{dest_location['lat']},{dest_location['lng']}"

    # 生成Google Maps導航URL
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"

    # 打開預設瀏覽器並導航到Google Maps URL
    webbrowser.open(maps_url)
    return f"導航到Google Maps: {maps_url}"
