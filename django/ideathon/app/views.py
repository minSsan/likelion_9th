from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

# used in 'makedb : API module'
from urllib.parse import urlencode, quote_plus, unquote
import xmltodict
import requests

# used in 'return_details'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import json, random
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
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
    infos = hospital.objects.all()
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    op = request.GET.get('op', '')

    if op:
        infos = infos.filter(
            Q(Name__icontains = '소아' or '어린이') |
            Q(Etc__icontains = '소아' or '어린이') |
            Q(Info__icontains = '소아' or '어린이') |
            Q(dgsb__icontains = '소아' or '어린이') 
        ).distinct()
    
    if kw:
        infos = infos.filter(
            Q(Name__icontains = kw) |
            Q(Etc__icontains = kw) |
            Q(Info__icontains = kw) |
            Q(dgsb__icontains = kw) 
        ).distinct()

    paginator = Paginator(infos, 10)
    posts = paginator.get_page(page)
    context = {
        'infos':infos,
        'posts':posts,
        'kw' : kw,
        'op' : op,
    }
    return render(request, "info_list.html", context)

def info_list_detail(request, id):
    infos = get_object_or_404(hospital, pk=id)
    context = {
        'infos' : infos,
    }
    return render(request, "info_list_detail.html", context)

# 상세 페이지 호출
def detail(request, keyword, place_name, address):
    return render(request, "detail.html")


def getData(request, keyword, addr, place_name):
    wordChange = str.maketrans('+', ' ')
    # parameters (함수로 만들어질 때 파라미터로 사용 될 변수들임)
    name = place_name.translate(wordChange)
    address = addr.translate(wordChange)
    address = address.split(" ")[1]

    if keyword == '응급실':
        name = name.replace('서울대', '서울대학교').split(" ")[0][:5]

        # hpid 검색
        xmlUrl = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire'
        key = unquote('5QlhomHsza06IR+wqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW/OQunOEnAb+AOYSlEWKVL8HVw93hpg==')
        # key = unquote('5QlhomHsza06IR%2BwqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW%2FOQunOEnAb%2BAOYSlEWKVL8HVw93hpg%3D%3D')

        queryParams = '?' + urlencode(
            {
                # 항목 코드 : 값
                quote_plus('ServiceKey') : key, 
                quote_plus('Q0') : address,
                #quote_plus('Q1') : '분당구',
                quote_plus('QN') : name,
            }
        )   

        # xml 파싱
        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        dataList = xmlDict['response']['body']['items']['item']
        if type(dataList) == dict:
            hpid = dataList['hpid']
        else :
            hpid = dataList[0]['hpid']


        # 실시간 응급실 가용병상 정보
        xmlUrl = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire'

        queryParams = '?' + urlencode(
            {
                # 항목 코드 : 값
                quote_plus('ServiceKey') : key, 
                quote_plus('STAGE2') : address,
                quote_plus('numOfRows') : '100',
            }
        )
        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        dataList = xmlDict['response']['body']['items']['item']
        
        if type(dataList) != dict:
            data = next((item for item in dataList if item['hpid'] == hpid), None)
        else :
            data = dataList

        if data != None:
            # 진료과목 검색
            xmlUrl = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytBassInfoInqire'

            queryParams = '?' + urlencode(
                {
                    # 항목 코드 : 값
                    quote_plus('ServiceKey') : key, 
                    quote_plus('HPID') : hpid,
                }
            )

            # xml 파싱
            response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

            xmlDictPre = xmltodict.parse(response)
            xmlJsonPre = json.dumps(xmlDictPre)
            xmlDict = json.loads(xmlJsonPre)
            dgid = xmlDict['response']['body']['items']['item']['dgidIdName']
            
            data['dgid'] = dgid
            data['keyword'] = keyword
        
        info = json.dumps(data, ensure_ascii=False)
        return HttpResponse(info)
        
    elif keyword == '약국':

        xmlUrl = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire'
        key = unquote('5QlhomHsza06IR+wqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW/OQunOEnAb+AOYSlEWKVL8HVw93hpg==')

        queryParams = '?' + urlencode(
                {
                    # 항목 코드 : 값
                    quote_plus('ServiceKey') : key, 
                    quote_plus('Q1') : address,
                    quote_plus('QN') : name,
                    quote_plus('pageNo') : '1',
                    quote_plus('numOfRows') : '1',
                }
            )

        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        dataList = xmlDict['response']['body']['items']['item']

        getList = ['dutyAddr', 'dutyName', 'dutyTel1', 'dutyTime1c', 'dutyTime1s', 'dutyTime2s','dutyTime2c', 'dutyTime3s', 'dutyTime3c', 'dutyTime4s', 'dutyTime4c', 'dutyTime5s', 'dutyTime5c', 'dutyTime6s', 'dutyTime6c', 'dutyTime7s', 'dutyTime7c', 'dutyTime8c','dutyTime8s', 'dutymapimg']
        data = {}

        for i in getList :
            data[i] = dataList.get(i, '')

        data['keyword'] = keyword

        info = json.dumps(data, ensure_ascii=False)
        return HttpResponse(info)

    else:
        xmlUrl = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire'
        key = unquote('5QlhomHsza06IR+wqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW/OQunOEnAb+AOYSlEWKVL8HVw93hpg==')
        name = name.replace('서울대', '서울대학교').split(" ")[0][:5]
        
        queryParams = '?' + urlencode(
            {
                # 항목 코드 : 값
                quote_plus('ServiceKey') : key, 
                quote_plus('Q0') : address,
                #quote_plus('Q1') : '분당구',
                quote_plus('QN') : name,
            }
        )   

        # xml 파싱
        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        dataList = xmlDict['response']['body']['items']['item']

        if type(dataList) == dict:
            hpid = dataList['hpid']
        else :
            hpid = dataList[0]['hpid']

        xmlUrl = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlBassInfoInqire'

        queryParams = '?' + urlencode(
            {
                # 항목 코드 : 값
                quote_plus('ServiceKey') : key, 
                quote_plus('HPID') : hpid,
            }
        )
        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        dataList = xmlDict['response']['body']['items']['item']

        getList = ['dutyAddr', 'dutyName', 'dutyTel1', 'dutyTime1c', 'dutyTime1s', 'dutyTime2s','dutyTime2c', 'dutyTime3s', 'dutyTime3c', 'dutyTime4s', 'dutyTime4c', 'dutyTime5s', 'dutyTime5c', 'dutyTime6s', 'dutyTime6c', 'dutyTime7s', 'dutyTime7c', 'dutyTime8c','dutyTime8s', 'dutymapimg', 'dgidIdName', 'dutyInf']
        data = {}

        for i in getList :
            data[i] = dataList.get(i, '')

        data['keyword'] = keyword

        info = json.dumps(data, ensure_ascii=False)
        return HttpResponse(info)


def makedb(request): #데이터 생성함수 http://127.0.0.1:8000/makedb 로 접속하여 생성
    
    error_count = 0
    # key = unquote('5QlhomHsza06IR%2BwqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW%2FOQunOEnAb%2BAOYSlEWKVL8HVw93hpg%3D%3D')
    xmlUrl = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire'
    xmlUrl2 = 'http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1'
    xmlUrl3 = 'http://apis.data.go.kr/B551182/medicInsttDetailInfoService/getFacilityInfo'
    xmlUrl4 = 'http://apis.data.go.kr/B551182/medicInsttDetailInfoService/getDetailInfo'
    xmlUrl5 = 'http://apis.data.go.kr/B551182/medicInsttDetailInfoService/getMdlrtSbjectInfoList'
    xmlUrl6 = 'http://apis.data.go.kr/B551182/medicInsttDetailInfoService/getSpcHospAppnFieldList'
    key = unquote('5QlhomHsza06IR+wqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW/OQunOEnAb+AOYSlEWKVL8HVw93hpg==')
    key2 = unquote('5QlhomHsza06IR%2BwqKACS07lSsg0Pl9pAzf6jg137KsfPwRnlvGqgdYW%2FOQunOEnAb%2BAOYSlEWKVL8HVw93hpg%3D%3D')

    num = random.sample(range(1, 72865), 15)
    for i in range(len(num)) :
        queryParams = '?' + urlencode(
            {
                quote_plus('ServiceKey') : key, 
                quote_plus('pageNo') : num[i],
                quote_plus('numOfRows') : '1',
            }
        )

        response = requests.get(xmlUrl + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)
        data = xmlDict['response']['body']['items']['item']


        #####
        queryParams = '?' + urlencode(
            {
                quote_plus('ServiceKey') : key2,
                quote_plus('pageNo') : '1', 
                quote_plus('numOfRows') : '1',
                quote_plus('yadmNm') : data['dutyName'][:5],
                quote_plus('xPos') : data['wgs84Lon'],
                quote_plus('yPos') : data['wgs84Lat'],
                quote_plus('radius') : '50',
            }
        )

        response = requests.get(xmlUrl2 + queryParams).text.encode('utf-8')

        xmlDictPre = xmltodict.parse(response)
        xmlJsonPre = json.dumps(xmlDictPre)
        xmlDict = json.loads(xmlJsonPre)

        if xmlDict['response']['body']['items'] == None :
            print('조회 오류')
            error_count += 1
        else :
            data2 = xmlDict['response']['body']['items']['item']
            # drTotCnt 의사총수 mdeptSdrCnt 의과전문의 detySdrCnt 치과전문의 cmdcSdrCnt 한방전문의

            #####
            queryParams = '?' + urlencode(
                {
                    quote_plus('ServiceKey') : key2, 
                    quote_plus('numOfRows') : '99',
                    quote_plus('PageNo') : '1',
                    quote_plus('ykiho') : data2['ykiho'],
                }
            )

            response = requests.get(xmlUrl3 + queryParams).text.encode('utf-8')

            xmlDictPre = xmltodict.parse(response)
            xmlJsonPre = json.dumps(xmlDictPre)
            xmlDict = json.loads(xmlJsonPre)
            data3 = xmlDict['response']['body']['items']['item']
            # hghrSickbdCnt 일반입원실상급병상수 stdSickbdCnt 일반입원실일반병상수 aduChldSprmCnt 성인중환자병상수 nbySprmCnt 신생아중환자병상수
            # partumCnt 분만실병상수 soprmCnt 수술실병상수 emymCnt 응급실병상수 ptrmCnt 물리치료실병상수 chldSprmCnt 소아중환자병상수
            # psydeptClsHigSbdCnt 정신과폐쇄상급병상수 psydeptClsGnlSbdCnt 정신과폐쇄일반병상수 isnrSbdCnt 격리실병상수 anvirTrrmSbdCnt 무균치료실병상수

            response = requests.get(xmlUrl4 + queryParams).text.encode('utf-8')

            xmlDictPre = xmltodict.parse(response)
            xmlJsonPre = json.dumps(xmlDictPre)
            xmlDict = json.loads(xmlJsonPre)

            if xmlDict['response']['body']['items'] != None :
                data4 = xmlDict['response']['body']['items']['item']
            else :
                data4 = {}  
            # emyDayYn 주간응급실운영여부 emyNgtYn 야간응급실운영여부 parkQty 주차가능대수

            response = requests.get(xmlUrl5 + queryParams).text.encode('utf-8')

            xmlDictPre = xmltodict.parse(response)
            xmlJsonPre = json.dumps(xmlDictPre)
            xmlDict = json.loads(xmlJsonPre)

            if xmlDict['response']['body']['items'] != None :
                data5 = xmlDict['response']['body']['items']['item']
            else :
                data5 = {}

            
            #진료가능과목
            if type(data5) == list :
                dgsbjtCdNm = "" 
                for j in range(len(data5)):
                    dgsbjtCdNm += data5[j]['dgsbjtCdNm']
                    dgsbjtCdNm += ' '
            else :
                dgsbjtCdNm = data5.get('dgsbjtCdNm', "")

            queryParams = '?' + urlencode(
                {
                    quote_plus('ServiceKey') : key2, 
                    quote_plus('numOfRows') : '99',
                    quote_plus('PageNo') : '1',
                    quote_plus('ykiho') : data2['ykiho'],
                }
            )

            response = requests.get(xmlUrl6 + queryParams).text.encode('utf-8')

            xmlDictPre = xmltodict.parse(response)
            xmlJsonPre = json.dumps(xmlDictPre)
            xmlDict = json.loads(xmlJsonPre)

            if xmlDict['response']['body']['items'] != None :
                data6 = xmlDict['response']['body']['items']['item']
            else :
                data6 = {}

            #전문병원지정분야
            if type(data6) == list :
                srchCdNm = '' 
                for k in range(len(data6)) :
                    srchCdNm += data6[k]['srchCdNm']
                    srchCdNm += ' '
            else :
                srchCdNm = data6.get('srchCdNm')

            new_data = hospital()
            new_data.Name = data.get('dutyName')
            new_data.Addr = data.get('dutyAddr')
            new_data.Tele = data.get('dutyTel1')
            new_data.Mono = data.get('dutyTime1s', '')
            new_data.Monc = data.get('dutyTime1c', '')
            new_data.Tueo = data.get('dutyTime2s', '')
            new_data.Tuec = data.get('dutyTime2c', '')
            new_data.Wedo = data.get('dutyTime3s', '')
            new_data.Wedc = data.get('dutyTime3c', '')
            new_data.Thuo = data.get('dutyTime4s', '')
            new_data.Thuc = data.get('dutyTime4c', '')
            new_data.Frio = data.get('dutyTime5s', '')
            new_data.Fric = data.get('dutyTime5c', '')
            new_data.Sato = data.get('dutyTime6s', '')
            new_data.Satc = data.get('dutyTime6c', '')
            new_data.Suno = data.get('dutyTime7s', '')
            new_data.Sunc = data.get('dutyTime7c', '')
            new_data.Holo = data.get('dutyTime8s', '')
            new_data.Holc = data.get('dutyTime8c', '')
            new_data.Hpid = data.get('hpid', '')
            new_data.Etc = data.get('dutyEtc', '')
            new_data.Info = data.get('dutyInf', '')
            new_data.Map = data.get('dutyMapimg', '')

            new_data.Todr = data2.get('drTotCnt', '')
            new_data.medr = data2.get('mdeptSdrCnt', '')
            new_data.dedr = data2.get('detySdrCnt', '')
            new_data.cmdr = data2.get('cmdcSdrCnt', '')

            new_data.hgSi = data3.get('hghrSickbdCnt', '')
            new_data.stSi = data3.get('stdSickbdCnt', '')
            new_data.adSp = data3.get('aduChldSprmCnt', '')
            new_data.nbSp = data3.get('nbySprmCnt', '')
            new_data.paCn = data3.get('partumCnt', '')
            new_data.soCn = data3.get('soprmCnt', '')
            new_data.emCn = data3.get('emymCnt', '')
            new_data.ptCn = data3.get('ptrmCnt', '')
            new_data.chCn = data3.get('chldSprmCnt', '')
            new_data.pshgCn = data3.get('psydeptClsHigSbdCnt', '')
            new_data.psstCn = data3.get('psydeptClsGnlSbdCnt', '')
            new_data.isCn = data3.get('isnrSbdCnt', '')
            new_data.anCn = data3.get('anvirTrrmSbdCnt', '')

            new_data.emDy = data4.get('emyDayYn', 'N')
            new_data.emNg = data4.get('emyNgtYn', 'N')
            new_data.paQt = data4.get('parkQty', '')
            new_data.dgsb = dgsbjtCdNm
            new_data.srch = srchCdNm


            new_data.save()
            print(i)

    return render(request)