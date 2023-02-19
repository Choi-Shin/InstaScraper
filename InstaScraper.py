from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import time
import os
import json
import urllib.request

# instagram json으로 바꾸는 링크
jsonLink = "?__a=1&__d=dis"


load_dotenv(verbose=True)

driver_path = os.getenv("DRIVER_PATH")
dir_name = os.getenv("FILEPATH") + "/result"
ID = os.getenv("ID")
PASSWORD = os.getenv("PASSWORD")
SCROLL_PAUSE_TIME = int(os.getenv("PAUSE_TIME"))
TARGET_PAGE = os.getenv("TARGET_PAGE")

option = Options()
option.add_argument("--incognito")
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-setuid-sandbox")
option.add_argument('--disable-dev-shm-usage')
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
s = Service(
    executable_path=driver_path)
driver = webdriver.Chrome(service=s, options=option)
driver.implicitly_wait(10)

link_arr = []


def login():
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    id = driver.find_element(by=By.NAME, value='username')
    id.send_keys(ID)
    pw = driver.find_element(by=By.NAME, value='password')
    pw.send_keys(PASSWORD)
    time.sleep(1)
    pw.submit()
    time.sleep(5)
    driver.find_elements(by=By.TAG_NAME, value="button")[1].click()


def 링크가져오기():
    # 텍스트 = 본문.text
    링크 = driver.find_elements(by=By.TAG_NAME, value="a")
    for l in 링크:
        link = l.get_attribute("href")
        if link.startswith("https://www.instagram.com/p/"):
            if not link in link_arr:
                link_arr.append(link)


def 스크롤내리기():
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    링크가져오기()
    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        링크가져오기()
        print(link_arr)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height


def 사진넘기기():
    버튼 = driver.find_element(by=By.CSS_SELECTOR, value='._6CZji')
    버튼.click()
    time.sleep(2)


def 중복제거하기(link_list):
    new_list = []
    for l in link_list:
        print(l)
        if not (l in new_list):
            new_list.append(l)
        else:
            continue
    return new_list


def makeDir():
    time.sleep(1.5)
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print('이미 존재하는 폴더입니다.')


def makeSubDir(folderNum):
    path = f"{dir_name}/{folderNum}"
    try:
        os.mkdir(path)
    except FileExistsError:
        print("Directory exists already")
    return path


def downloadMediaWithJson(d):
    n = 1
    data = d["items"][0]
    try:
        count = data["carousel_media_count"]
        for c in range(0, count):
            mediaType = data["carousel_media"][c]["media_type"]
            if mediaType == 1:
                imgUrl = data["carousel_media"][c]["image_versions2"]["candidates"][0]["url"]
                # a function to save image
                downloadImage(path, imgUrl, n)
                n += 1
            elif mediaType == 2:
                videoUrl = data["carousel_media"][c]["video_versions"][0]["url"]
                downloadVideo(path, videoUrl, n)
                n += 1
    except:
        mediaType = data["media_type"]
        if mediaType == 1:
            imgUrl = data["image_versions2"]["candidates"][0]["url"]
            # a function to save image
            downloadImage(path, imgUrl, n)
            n += 1
        elif mediaType == 2:
            videoUrl = data["video_versions"][0]["url"]
            downloadVideo(path, videoUrl, n)
            n += 1
    try:
        text = data["caption"]["text"]
        getTextOfPost(path, text)
    except:
        pass


def downloadImage(path, url, n):
    savePath = f"{path}/{n}.jpeg"
    urllib.request.urlretrieve(url, savePath)
    print(savePath)


def downloadVideo(path, url, n):
    savePath = f"{path}/{n}.mp4"
    urllib.request.urlretrieve(url, savePath)
    print(savePath)


def getTextOfPost(path, content):
    if content is not None:
        with open(path + f"/text.txt", "w", encoding="UTF-8") as f:
            f.write(content)
        f.close()
        print(f"Saved successfully to {path}")


login()
# 페이지의 모든 게시물 링크 가져오기
driver.get(TARGET_PAGE)
time.sleep(2)
스크롤내리기()
time.sleep(2)
link_arr.reverse()

# 가져온 링크의 포스트를 json으로 응답 받아 이미지나 사진을 다운로드 받고 게시글 얻기
makeDir(dir_name)
folderNum = 1
for link in link_arr:
    path = makeSubDir(folderNum)
    folderNum += 1
    driver.get(f"{link + jsonLink}")
    jsonData = driver.find_element(by=By.XPATH, value="/html/body/pre").text
    data = json.loads(jsonData)
    downloadMediaWithJson(data)
    print(f"{path} 저장완료")
    time.sleep(2)
