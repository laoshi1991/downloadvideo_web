import requests
from fake_useragent import UserAgent

def get_bilibili_cookie():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.chrome,
        'Referer': 'https://www.bilibili.com/'
    }
    try:
        session = requests.Session()
        # 访问主页获取初始 Cookie (buvid3, b_nut 等)
        response = session.get('https://www.bilibili.com/', headers=headers, timeout=10)
        cookies = session.cookies.get_dict()
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        print(f"Captured Cookies: {cookie_str}")
        return cookie_str, headers['User-Agent']
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    get_bilibili_cookie()
