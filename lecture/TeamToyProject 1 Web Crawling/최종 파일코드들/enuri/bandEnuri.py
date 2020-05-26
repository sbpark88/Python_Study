#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# 1. 셀레니움 환경 구성

# 라이브러리 선언
import bs4
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
sleepTime1 = 1
sleepTime2 = 5
# 드라이버 위치 설정
driver_loc = "./chromedriver"
# driver_loc = "./chromedriver.exe"

# 드라이버 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument("window-size=1920x1080") # 파이썬이 크롬창을 띄울 것인데 창 크기 선택
# 리눅스처럼 웹 화면 없는 경우에도 실행 가능.
options.add_argument('headless')                           
options.add_argument('disable-gpu')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

# 웹 드라이버 정의
driver = webdriver.Chrome(driver_loc, options=options)



# 2. 스마트밴드 상품 목록 페이지로 이동

# 웹페이지 이동

# 에누리 웹페이지로 이동
enuriUrl = 'http://www.enuri.com/'
driver.get(enuriUrl)

# 창 최대화
driver.maximize_window()

# 태블릿/모바일 메뉴 클릭
catXpath = '//*[@id="gnbMenu"]/li[4]/a/em'
catMenu = driver.find_element_by_xpath(catXpath)
catMenu.click()

# 스마트워치 클릭
catSubXpath = '//*[@id="first_depth3"]/li[7]/p'
catSubMenu = driver.find_element_by_xpath(catSubXpath)

catTargetXpath = '//*[@id="first_depth3"]/li[7]/div/ul[2]/li[2]/a'
catTargetMenu = driver.find_element_by_xpath(catTargetXpath)

ActionChains(driver).move_to_element(catSubMenu).click(catTargetMenu).perform()
time.sleep(sleepTime1)

# 가격비교하여 보기
compareXpath = '//*[@id="tabsDiv"]/li[2]/a'
compareMenu = driver.find_element_by_xpath(compareXpath)
compareMenu.click()
time.sleep(sleepTime1)

# 90개씩 보기
viewXpath = '//*[@id="pageGapSelDiv"]/a'
viewMenu = driver.find_element_by_xpath(viewXpath)
viewMenu.click()
time.sleep(sleepTime1)

viewTargeXpath = '//*[@id="pageGapSelDiv"]/ul/li[3]/a'
viewTargetMenu = driver.find_element_by_xpath(viewTargeXpath)
viewTargetMenu.click()



# 3. 데이터 수집

rowList = []
titleList = []
nameList = []

# 페이지 url 추출 -> 페이지 이동 시 사용
pageUrl = driver.current_url

# 쿼리 key, value값 추출 -> 상품 페이지 이동 확인
cateNum = urlparse(pageUrl).query.split("&")[0].split("=")[1]

# # 반복문
count = 0
missCount = 0

for i in range(999):
    
    # 전체 상품 웹페이지 이동 설정
    pageNumUrl = pageUrl+'&page=' + str(i + 1)
    driver.get(pageNumUrl)
    time.sleep(sleepTime2)
    
    flag = True
    notFoundCount = 0
    while flag:
        
        # 전체 상품 웹페이지 소스코드 추출
        try:
            data = driver.page_source
            bs = bs4.BeautifulSoup(data, 'html.parser')

            pageSourceTag = bs.find('ul', {'id':'listBodyDiv'})       
            
            pageSourceItemTags = pageSourceTag.findAll('li', {'cate':cateNum})

            flag = False
        except:
            notFoundCount += 1
            print("Not Found", notFoundCount)
            print("reSearch!!")
            time.sleep(sleepTime1)
            if notFoundCount > 6:
                break
            continue
    
    pageSourceItemTagsLen = len(pageSourceItemTags)
    # 전체 상품 웹페이지가 존재하지 않는 경우 break
    if pageSourceItemTagsLen == 0:
        break
    
    # 모든 상품의 정보를 긁어 옴.
    for j in range(pageSourceItemTagsLen):
        # 스마트 밴드가 아닌 상품 제외
        try:
            passCertain = pageSourceItemTags[j].findAll('div',{'class':'summary'})[1].find('b')
        except:
#             missCount += 1
#             print("스마트밴드 아님 제외!!", liTags[j], missCount)
            continue               
        
        # 상품 페이지로 이동
        itemId = pageSourceItemTags[j].attrs['id']
        itemXpath = '//*[@id="{}"]/div[1]/strong/a'.format(itemId)

        itemMenu = driver.find_element_by_xpath(itemXpath)
        itemMenu.click()
        
        # 상품 페이지로 포커스 이동
        driver.switch_to.window(driver.window_handles[-1])

                    
            
        searchFlag = True
        notFoundCount = 0
        
        # 아이템 페이지에서 소스코드를 불러올 때까지 반복문 실행(7회로 횟수 제한)
        while (searchFlag):
            try:
                data = driver.page_source
                bs = bs4.BeautifulSoup(data, 'html.parser')
                divTag = bs.find("div", attrs={"class":"malllowprice"})
                div2Tag = divTag.find("div", {"class":"malllow__cont"})
                tableTag = div2Tag.find('table', {'class':'malllow__list'})
                tbodyTag = tableTag.find('tbody', {'id':'vip_malllow_item_list_id'})
                trTag = tbodyTag.find('tr')
                tdTag = trTag.find('td', {'class':'malllow__item price'})

                # 소스코드 불러온 경우 반복문 탈출
                searchFlag = False
            except:
                notFoundCount += 1
                print("Not Found", notFoundCount)
                print("reSearch!!")
                
                time.sleep(sleepTime1)
                
                # 시도횟수가 7회를 넘어간 경우 상품 페이지 탈출
                if notFoundCount > 6:
                    break
                    
                continue
        
        # 한 상품의 컬럼명과 스펙정보를 담을 리스트 생성
        columnList = []
        titleColumnList = []
        
        # 최저가 및 최저가 컬럼명 추출
        lowestPriceTitle = tdTag.find('span').text
        titleColumnList.append(lowestPriceTitle)
        lowestPrice = tdTag.find('strong').text.replace(',','')
        columnList.append(lowestPrice)

        # 상품명 및 상품명 컬럼명 추출
        titleNameDivTag = bs.find("div", {"class":"prdcinfo"})
        titleNameDiv2Tag = titleNameDivTag.find("div", {"class":"prdcinfo__tit"})
        titleNameH3Tag = titleNameDiv2Tag.find("h3", {"class":"prdcname"})
        titleName = titleNameH3Tag.text.strip().split("[")[0].replace(" ","")
        columnList.append(titleName)
        titleColumnList.append("상품명")
        
        # 제조사 및 제조사 컬럼명 추출
        makerNameDivTag = bs.find("div", {"id":"prdinfo_vip_attribute"})
        makerNameDiv2Tag = makerNameDivTag.find("div", {"class":"summary"})
        makerNameList = makerNameDiv2Tag.text.strip().split("|")[0].replace(" ","").split(":")
        
        # 제조사 
        if len(makerNameList) > 0:
            makerNameTitle = makerNameList[0]
            if makerNameTitle == "제조사":
                makerName = makerNameList[1]
                columnList.append(makerName)
                titleColumnList.append(makerNameTitle)

        # 상품 상세 정보 테이블 태그 추출
        itemDivTag = bs.find('div', {'id':'enuri_spec_table'})
        itemTableTag = itemDivTag.findAll('table', {'class':'offerer__table'})
        
        
        itemTableTagLen = len(itemTableTag)
        
        # 상세 정보 테이블에서 스펙 정보 추출
        for k in range(itemTableTagLen):
            
            # 상품 상세 정보 테이블이 있는 경우만 추출
            if None != itemTableTag[k]:
                itemTbodyTag = itemTableTag[k].find('tbody')
                itemThTags = itemTbodyTag.findAll('th', {'scope':'row'})
                itemTdTags = itemTbodyTag.findAll('td')
                
                itemThTagsLen = len(itemThTags)
                for l in range(itemThTagsLen):
                    
                    # 상품 상세 정보 테이블 내용 추출
                    if itemThTags[l].text.strip() != '':
                        commaList =  itemTdTags[l].text.strip().replace('\t','').split(",")
                        commaListLen = len(commaList)
                        
                        if commaListLen == 1:
                            itemCount = titleColumnList.count(itemThTags[l].text.strip())
                        
                            if itemCount > 0:
                                titleColumnList.append(itemThTags[l].text.strip() + str(itemCount + 1))
                            else:
                                titleColumnList.append(itemThTags[l].text.strip())
                            
                            columnList.append(itemTdTags[l].text.strip().replace('\t',''))
                            
                        else:
                            for m in range(commaListLen):
                                titleColumnList.append(commaList[m].strip())
                                columnList.append("O")

                        
        count += 1
                        
                        
# 디버깅용                        
#         print(len(columnList), "확인하기!!")
#         print(len(titleList))
#         print(columnList)
#         print(titleList)
#         print(len(titleList))
#         print(columnList)

        # 모든 상품의 컬럼 리스트와 컬럼 정보 리스트에 삽입 
        titleList.append(titleColumnList)
        rowList.append(columnList)

        print(titleColumnList)
        print(columnList)
        print(count)
        
        # 포커스 맞춰진 창을 닫고 기존의 전체 상품 웹페이지로 다시 이동
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


# 4. 상품당 컬럼 수 동일화 및 컬럼 정렬

titleListLen = len(titleList)

# 정렬할 기준컬럼을 만듦. 첫번째 상품의 컬럼명에 다른 모든 상품들의 컬럼명 정보를 삽입한다.
for i in range(titleListLen):
    titleListILen = len(titleList[i])
    for j in range(titleListILen):
        if not titleList[i][j] in titleList[0]:
            titleList[0].append(titleList[i][j])
            rowList[0].append('')
                
# 기준컬럼리스트에 맞게 모든 상품의 컬럼리스트를 동일하게 만든다.
for i in range(titleListLen):
    for j in range(len(titleList[0])):
        # 중복요소 고려!!
        if not titleList[0][j] in titleList[i]:
            titleList[i].append(titleList[0][j])
            rowList[i].append('')

# 모든 상품의 컬럼리스트를 동일하게 정렬한다.
for i in range(titleListLen):
    for j in range(len(titleList[0])):
        if titleList[0][j] != titleList[i][j]:
            tmpTitleIndex = titleList[i].index(titleList[0][j]) # index 5
            tmpTitle = titleList[i][j] # 4
            titleList[i][j] = titleList[0][j] # 1
            titleList[i][tmpTitleIndex] = tmpTitle # 4

            tmpIndex = tmpTitleIndex
            tmp = rowList[i][j]
            rowList[i][j] = rowList[0][j]
            rowList[i][tmpIndex] = tmp

# 데이터 정제
for i in range(len(rowList)):
    if len(rowList[i]) != len(titleList[0]):
        print("false", i)
        del rowList[i]

            
# 데이터 프레임 저장
smartBandEnuriData = pd.DataFrame(rowList, columns=titleList[0])
smartBandEnuriData.to_csv('smartBandEnuriData.csv', index = False , encoding = 'utf-8')

