from django.shortcuts import render
from django.core.paginator import Paginator

# used in 'return_details'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import json

from django.shortcuts import render
from .models import *

def main(request):
    medicals = Medical.objects.all()
    context = {
        'medicals':medicals,
    }
    return render(request, 'main.html', context)

def map(request, keyword):
    context = {
        'keyword' : keyword
    }
    return render(request, "map.html", context)

def search(request):
    return render(request, "search.html")

def info_list(request):
    infos = Detail.objects.all()
    paginator = Paginator(infos, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'infos':infos,
        'posts':posts,
    }
    return render(request, "info_list.html", context)

# 상세 페이지 호출
def detail(request, keyword, place_name, address):
    return render(request, "detail.html")


'''
def return_details(name, address):
    # parameters (함수로 만들어질 때 파라미터로 사용 될 변수들임)
    # name = "한마음소아청소년과의원"
    # address = "경기 안산시 단원구 광덕동로 75"

    # webdriver 옵션에서 headless 기능을 사용할 것임. headless: 브라우저를 띄우지 않음
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')

    # chromedriver의 경로를 저장.
    chromedriver = 'C:\chromedriver\chromedriver.exe'

    # headless 옵션으로 드라이버를 호출한다. => 브라우저 화면에 띄우지 않음
    driver = webdriver.Chrome(executable_path=chromedriver, options=webdriver_options)

    # 테스트용
    # driver = webdriver.Chrome(executable_path=chromedriver)

    wait = WebDriverWait(driver, 5)

    driver.implicitly_wait(3)

    # 네이버 지도를 브라우저에 실행시킴
    driver.get("https://map.naver.com/v5/")

    # 검색창 태그를 input_element 라는 변수에 저장함
    input_element = driver.find_element_by_css_selector('.input_box > input')
    input_element.send_keys(address + " " + name)
    input_element.send_keys(Keys.RETURN) # 네이버 지도는 엔터키로 검색이 동작됨. -> Keys.RETURN(ENTER 키) 사용

    # 현재 찾고자 하는 요소는 searchIframe에 존재 => frame을 switch 하는 작업 필요
    wait.until(ec.frame_to_be_available_and_switch_to_it('searchIframe'))

    # driver.find_element_by_css_selector('#_pcmap_list_scroll_container > ul > li:nth-child(1) > div._7jQRv._2mQIf > div._1uXIN > a').click()

    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/ul/li[1]/div[2]/div[1]/a').click()

    # 위치 정보는 entryIframe에 있기 때문에, 외부 프레임으로 다시 이동한 다음 entryIframe으로 이동시킴
    driver.switch_to.default_content()
    wait.until(ec.frame_to_be_available_and_switch_to_it('entryIframe'))

    # description 내용 먼저 펼치기 (<- description 세부 정보를 클릭하면 html 코드가 변경됨)
    driver.find_element_by_css_selector("a.M_704").click()

    # description을 펼친 상태에서 html을 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        open_time = soup.select_one('span._20pEw').get_text()
    except: # 영업시간 정보가 기재되어 있지 않은 경우
        open_time = ""

    try:
        homepage = soup.select_one('a._1RUzg').get_text()
    except: # 홈페이지가 없는 경우
        homepage = ""

    try:
        description = soup.select_one('span.WoYOw').get_text()
    except: # description 정보가 기재되어있지 않은 경우
        description = ""

    try:
        table = soup.find('table')
    except: # 테이블이 없는 경우(약국)
        table = ""

    context = {
        'place_name':name,
        'address':address,
        'telephone':soup.select_one('span._3ZA0S').text,
        'open_time':open_time,
        'homepage':homepage,
        'description':description,
        'table':table,
    }

    return context
'''