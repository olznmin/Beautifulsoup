# selenium, bs4 , chrome driver 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import time
import json

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# 터미널에서 URL 입력 받기
# url = input("웹 페이지 URL을 입력하세요: ")

# http://gcorner.gmarket.co.kr/Bestsellers/Category

# 웹페이지 해당 주소 이동
browser.get('https://weverseshop.io/en/shop/GL_KRW/artists/2/categories/447')

#페이지 로딩을 위한 대기 시간 설정
time.sleep(5)

# 페이지 소스코드 가져오기
html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')

product_information = []

#제목, 가격 code 
li_tags = soup.find_all('li',class_=["sc-ee91b503-2 kDyufS","sc-ee91b503-2 eUVlIv","sc-ee91b503-2 cMhsLw"])

for li in li_tags:
    a_tag = li.find('a')

    if a_tag:
        title = a_tag.get('title')

    if a_tag:
        Producut_url = a_tag.get('href')

    figure_tag = a_tag.find('figure')
    figcaption_tag = figure_tag.find('figcaption')
    div_tag = figcaption_tag.find('div', class_="sc-57be2f03-1 laZlVs")
    strong_tag = div_tag.find('strong')

    # price
    if strong_tag:
        price = strong_tag.text 

    # ImageURl
    imagediv_tag = figure_tag.find('div',class_="sc-1924ec88-2 ekqBnQ")
    span_tag = imagediv_tag.find('span')
    img_tag = span_tag.find('img')

    if img_tag:
        Url = img_tag.get('src')

    # div_tag = figure_tag.find("div")
    # span_tag = div_tag.find("span")
    # img_tag = span_tag.find("img")

    # if img_tag:
    #     Url= img_tag.get("src")
    
    """

        li -> a-> figure -> div -> span -> img 
        
        li -> a-> figure -> div -> spna -> img 

        마지막 3줄이 출력이 안되는 상황 

    """

    product_data = {"Title" : title ,"Price":price,"Product_URL":Producut_url, "Image_Url":Url}
    product_information.append(product_data)
        
print(product_information)

# 리스트를 JSON 형태로 변환합니다.
json_data = json.dumps(product_information , indent=4, ensure_ascii=False)

filename = input("저장할 파일명을 입력하세요: ")

# JSON 데이터를 파일에 저장합니다.
with open(f'{filename}.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("상품정보 URL을 저장 완료하였습니다.")