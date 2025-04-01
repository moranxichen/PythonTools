import os
import requests
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def extract_video_url(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    chromedriver_path = ChromeDriverManager().install()
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    driver.implicitly_wait(10)

    try:
        source_tag = driver.find_element(By.TAG_NAME, "source")
        video_url = source_tag.get_attribute("src")
    except:
        video_url = None

    driver.quit()
    return video_url


def get_unique_filename(save_dir):
    """ 确保 save_dir 目录存在，并返回唯一的文件名 """
    os.makedirs(save_dir, exist_ok=True)  # 确保目录存在
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # 获取当前时间
    return os.path.join(save_dir, f"douyin_video_{timestamp}.mp4")


def download_video(video_url, save_path):
    if not video_url:
        print("未找到视频链接，无法下载。")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.douyin.com/"
    }

    response = requests.get(video_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"视频下载完成: {save_path}")
    else:
        print(f"下载失败，状态码: {response.status_code}")


def share2links(text):
    pattern = r'https:\/\/v\.douyin\.com\/[a-zA-Z0-9]+\/'
    match = re.search(pattern, text)
    if match:
        print("找到的抖音链接:", match.group(0))
    else:
        print("没有找到匹配的抖音链接")
    return match.group(0) if match else None


def main():
    share = input("输入分享链接: ")
    links = share2links(share)

    if not links:
        print("请输入有效的抖音分享链接")
        return

    video_url = extract_video_url(links)

    if video_url:
        print("提取到的视频链接:", video_url)
        print("提取链接完成，准备开始下载")

        save_dir = input("请输入保存目录 (默认 ./videos/): ").strip() or "./videos/"
        save_path = get_unique_filename(save_dir)  # 确保目录存在

        download_video(video_url, save_path)
    else:
        print("未能提取到视频链接")


if __name__ == '__main__':
    main()
