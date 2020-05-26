#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 1. 셀레니움 환경 구성

# 라이브러리 선언
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import pandas as pd
import time
sleepTime = 0.5

# 드라이버 위치 설정
driver_loc = "./chromedriver"
# driver_loc = "./chromedriver.exe"

# 드라이버 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument("window-size=2280x1440") # 파이썬이 크롬창을 띄울 것인데 창 크기 선택
options.add_argument('headless')                           
options.add_argument('disable-gpu')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

# 웹 드라이버 정의
driver = webdriver.Chrome(driver_loc, options=options)



# 2. 스마트밴드 상품 목록 페이지로 이동

# 웹페이지 이동

# 다나와 홈페이지로 이동
danawaUrl = "http://www.danawa.com/"
driver.get(danawaUrl)

# 메인 메뉴 클릭
catMainXpath = '//*[@id="danawa_header"]/div[2]/div/div[1]/a/span[2]'
catMainMenu = driver.find_element_by_xpath(catMainXpath)
catMainMenu.click()
time.sleep(sleepTime)

# 태블릿/모바일 클릭
catSubXpath = '//*[@id="sectionExplodeLayer"]/div[1]/ul/li[3]/a'
catSubMenu = driver.find_element_by_xpath(catSubXpath)
catSubMenu.send_keys(Keys.ENTER)
time.sleep(sleepTime)

# 스마트워치 클릭 (.clikc()으로 이동시 플래시 광고가 뜨면 광고를 누르기 때문에 .send_keys로 이동)
catTargetXpath = '//*[@id="categoryExplodeLayer12"]/div[2]/div[2]/ul/li[2]/a'
catTargetMenu = driver.find_element_by_xpath(catTargetXpath)
catTargetMenu.send_keys(Keys.ENTER)
time.sleep(sleepTime)




# 3. 데이터 수집

rowList = []
colHeaderList = ['제품명','최저가','사이트주소']

for i in range(0, 999):

    try:
        # 전체 상품 웹페이지 이동 설정
        pageSelector = '#productListArea > div.prod_num_nav > div > div > a:nth-child(' + str(i + 1) + ')'
        page = driver.find_element_by_css_selector(pageSelector)
        page.click()
        time.sleep(sleepTime)

    except:
        break

    # 전체 상품 웹페이지 소스코드 변수에 저장
    smartWatchHtml = driver.page_source

    # 태그 정보만 추출하여 변수에 저장
    bs = bs4.BeautifulSoup(smartWatchHtml, 'html.parser')
    
    # 상품명 구하기
    productName = bs.select('div > div.prod_info > p > a')
    productLen = len(productName)

    # 상품 페이지에 확률적으로 보이지 않는 0번 상품이 존재하는 것을 처리
    if productLen > 30:
        startNum = 1
        endNum = productLen
    else:
        startNum = 0
        endNum = productLen 

    columnList = []
    

    for j in range(startNum, endNum):
        nameTmp = productName[j-1].text.strip()
        columnList.append(nameTmp)

        # a href 태그의 name 속성명의 속성값이 productName인 것을 이용
        driver.find_elements_by_name("productName")[j-1].click()
        time.sleep(sleepTime)
        
        # 탭 번호를 변수화
        firstTab = driver.window_handles[0]
        secondTab = driver.window_handles[1]

        driver.switch_to.window(secondTab)
        time.sleep(sleepTime)

        # 개별 상품 웹페이지 소스코드 변수에 저장
        eachBandHtml = driver.page_source

        # 태그 정보만 추출하여 변수에 저장
        bs = bs4.BeautifulSoup(eachBandHtml, 'html.parser')

        
        # 일시 품절을 제외하고 최저가와 구매 사이트 추출
        if bs.find('tr', {'class':'lowest'}) != None:    # 일시 품절이 아닌 경우

            # 최저가 추출
            lowestPrice = bs.find('span', {'class':'lwst_prc'})
            columnList.append(lowestPrice.find('em', {'class':'prc_c'}).text.replace(',',""))

            # 최저가 구매 사이트 추출
            lowestSite = bs.find('tr', {'class':'lowest'})
            columnList.append(lowestSite.find('a')['href'])

        else:    # 일시 품절인 경우 빈 문자열 처리

            outOfStock = bs.find('div',{'class':'lowest_area lowest_blank'})
            columnList.append(outOfStock.find('strong', {'class':'pnt'}).text)
            columnList.append('')

        
        # 상세 정보 테이블 추출
        tableTag = bs.find('table', {'class':'spec_tbl'})
        tbodyTag = tableTag.find('tbody')

        # 상세 정보 테이블에서 스펙 이름 추출
        tdTags = tbodyTag.findAll('td')
        thTags = tbodyTag.findAll('th', {'class':'tit'})

 
        for k in range(0, len(tdTags)):

            if thTags[k].text != '':

                # 첫 페이지, 첫 상품일 때만 스펙 이름을 컬럼헤더 리스트에 저장
                if (j - 1) == 0 and i == 0:
                    colHeaderList.append(thTags[k].text)
                    
                # 상세 정보 테이블에서 처음 값 중 제조사 이름만 추출 - '(제조사 웹 사이트 바로가기)' 제거
                if k == 0:
                    columnList.append(tdTags[k].text.strip().split(' ')[0])

                # 상세 정보 테이블에서 그 외 모든 값 추출
                else:    
                    columnList.append(tdTags[k].text)
                    
                    # 전체 상품 중 15개 정도가 '인프라'가 2개가 존재해서 삭제하는 로직
                    columnLen = len(columnList)
                    if columnLen == 82:
                        columnList.pop(8)

 

        rowList.append(columnList)
        columnList = []

        
        driver.close()
        driver.switch_to.window(firstTab)

        

# 4. 데이터 정제

## 연주차컬럼 정제. 20XX년 09월 -> 20XX09
yearweekIndex = 4    # rowList[i][4] 가 연주차 정보를 저장

totalProdcutLen = len(rowList)
for i in range(0, totalProdcutLen):
    rowList[i][yearweekIndex] = rowList[i][yearweekIndex].strip().replace('년 ','').replace('월','')
    
    
    
# 5. 데이터 저장
smartWatch = pd.DataFrame(rowList, columns = colHeaderList)
# smartWatch = pd.DataFrame(rowList)

smartWatch.to_csv('./smartWatch(danawa)ver.1.0.5.csv', index=False, encoding='utf-8') 

