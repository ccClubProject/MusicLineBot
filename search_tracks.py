from dotenv import load_dotenv  # 用於讀取.env文件中的環境變量
import os  # 用於訪問操作系統的環境變量
import base64  # 用於對客戶端ID和密鑰進編碼
import json  # 解析JSON
from requests import post, get  # 發送HTTP請求
import random
# 加載 .env 文件中的環境變量
load_dotenv()
# 讀取密鑰
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

# 取得access token
def get_token():
    # 將 client_id 和 client_secret 組合成字符串
    auth_string = client_id + ":" + client_secret
    # 字符串編碼成字節
    auth_bytes = auth_string.encode("utf-8")
    # 將字節編碼為base64格式的字符串
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    # API端點URL
    url = "https://accounts.spotify.com/api/token"
    # 設置HTTP標頭，「基本授權」和「內容類型」
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # 指定授權類型"client_credentials"
    data = {"grant_type": "client_credentials"}
    # 發送POST請求，並接收回應
    result = post(url, headers=headers, data=data)

# 檢查json_result是否包含'access token'，如果有則返回，否則異常
    try:
        # 解析回應JSON數據
        json_result = result.json()
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON response from token endpoint. Response content: " + result.text)

    # 檢查是否有 "access_token" 字段
    if "access_token" in json_result:
        token = json_result["access_token"]
        return token
    else:
        raise Exception("Could not get access token. Response: " + result.content.decode("utf-8"))

# 獲取Bearer授權的HTTP標頭
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# 隨機推薦音樂
def random_recommendations(token):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    # 可用的genres
    available_genres = [
        'acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal',
        'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop',
        'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country',
        'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney',
        'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro',
        'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge',
        'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays',
        'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian',
        'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay',
        'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age',
        'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film',
        'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b',
        'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance',
        'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep',
        'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop',
        'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music'
    ]

    # 隨機推薦5個genres
    seed_genres = random.sample(available_genres, 5)

    params = {
        'seed_genres': ','.join(seed_genres),
        'limit': 1
    }
    response = get(url, headers=headers, params=params)
    recommendations = response.json()
    track_info = recommendations['tracks'][0]
    track_name = track_info['name']
    artist_name = track_info['artists'][0]['name']
    track_url = track_info['external_urls']['spotify']
    track_image_url = track_info['album']['images'][0]['url']
    # 輸出字典格式
    output = {
        'title': track_name,
        'artist': artist_name,
        'image_url': track_image_url,
        'details_url': track_url
    }
    return output
# 透過音樂類型尋找曲目
def search_tracks_by_genre(genre, token,limit=10):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        'q': f'genre:"{genre}"',
        'type': 'track',
        'limit': limit
    }
    response = get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['tracks']['items']:
            track_info = random.choice(result['tracks']['items'])
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            track_url = track_info['external_urls']['spotify']
            track_image_url = track_info['album']['images'][0]['url']

            # 輸出字典格式
            output = {
                'title': track_name,
                'artist': artist_name,
                'image_url': track_image_url,
                'details_url': track_url
            }
            return output
        else:
            return None
    else:
        return None
