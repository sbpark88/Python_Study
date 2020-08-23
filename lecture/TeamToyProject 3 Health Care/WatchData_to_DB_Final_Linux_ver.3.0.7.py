#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# # 1. 라이브러리 선언

# In[17]:


import pandas as pd
import os
import re

from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from datetime import datetime
from glob import glob
import time
import math
from db_connect_variables import connect_lnfo as db_login

# # 2. 함수 정의

# ## 2-1. 디렉토리를 리스트로 추출하는 함수

# In[2]:


# 캐시 파일 등은 제외하고 디렉토리만 리스트로 추출하는 함수
def findDir(pwd):
    directory = []
    try:
        totalDir = os.listdir(pwd)
    except Exception as e:
        print(e)
        
    for eachDir in totalDir:
        fullDir = os.path.join(pwd, eachDir)
        if os.path.isdir(fullDir):
            directory.append(eachDir)

    return directory

# 입력 받은 디렉토리(pwd)와 그 하위 디렉토리 목록(subDir)을 입력 받아 경로를 merge 시켜 리스트로 반환
def mergeSubDirList(pwd, subDir):
    reDefinedDir = []
    
    for eachDir in subDir:
        reDefinedDir.append(os.path.join(pwd, eachDir))
    
    return reDefinedDir

# 대상 경로를 입력해주면 해당 경로의 하위의 하위 디렉토리까지 리스트로 반환
def findTreeDir(pwd):
    # 인풋 파라미터의 디렉토리 내의 디렉토리를 리스트로 만들어 병합
    subDir = findDir(pwd)
    subDirList = mergeSubDirList(pwd, subDir)
    
    # 위 디렉토리 리스트 내의 디렉토리를 다시 한 번 리스트로 만들어 병합
    treeDirList = []
    for each in subDirList:
        subDirList = findDir(each)
        treeDirList.append(mergeSubDirList(each, subDirList))

    return treeDirList

# 최신 디렉토리만 리스트로 반환
def findLatest(categories, index):
    result = []

    for eachList in categories:
        eachList.sort()
        try:
            result.append(eachList[-index])
        except Exception as e:
            result.append(eachList[0])
            print(e)

    return result

# 입력 받은 디렉토리에서 CSV 파일만 전체 디렉토리 리스트로 추출
def findCsv(pwd):
    try:
        fileList = os.listdir(pwd)
        csvList = [file for file in fileList if (file.endswith(".csv")) \
                   and (file.split("\\")[-1].split(".")[0] == "com")\
                    and (re.search("(food|breath|reward|hist|recommend)", file) is None)]
    except Exception as e:
        print(e)
    
    return csvList

# 입력 받은 디렉토리 내에 csv 파일을 찾아 전체 디렉토리를 리스트로 반환
def findCsvDir(pwd):
    # 디렉토리 내 csv 파일을 리스트로 반환
    try:
        csvList = findCsv(pwd)
    except Exception as e:
        print(e)
    try:
        csvPathList = mergeSubDirList(pwd, csvList)
    except Exception as e:
        print(e)

    return csvPathList


# ## 2-2. 데이터 정제 함수

# In[20]:


# 컬럼명 정제 : 컬럼명 유형이 com.samsung.shealth.calories_burned.active_calorie인 경우 active_calorie만 추출
def splitColumn(columnList):
    for idx, val in enumerate(columnList):
        if re.search("com.", val) is not None:
            try:
                columnList[idx] = val.split(".")[-1]
            except Exception as e:
                print(e)
    return columnList

# dateToDatetime 함수에 보낼 _time 컬럼을 추출
def targetTimeCol(list):
    listLen = len(list)
    targetColList = []
    for i in range(listLen):
        if re.search("(time|date|duration)", list[i]) is not None:
            targetColList.append(list[i])
    return targetColList

# milliseconds -> minutes로 변경
def convertMillis(millisec):
    minutes=(millisec/(1000*60))
    return str(minutes)

# time 데이터 형식 일치 (2020. 07. 14 형식이나 timestamp 형식을 2020-07-14 형식으로 통일)
def dateTodatetime(date):
    date = str(date)
    result = None
    if re.search("\d{4}. \d{2}. \d{2}", date) is not None: # 시간 형식이 2020. 07. 08. ~인 경우에 대해서만
        splitDate = [each.strip() for each in date.split('.')]
        splitDateLen = len(splitDate)
        
        yearMonthDay = "-".join(splitDate[:splitDateLen - 1])
        hourMinSec = [each for each in splitDate[-1].split(":")]

        if "오후" in hourMinSec[0]:
            hourMinSec[0] = str(int(hourMinSec[0].split(" ")[-1]) + 12)
        elif ("오전" or "오후 12") in hourMinSec[0]:
            hourMinSec[0] = str(int(hourMinSec[0].split(" ")[-1]))
            
        hourMinSec = ":".join(hourMinSec)
        result = yearMonthDay + " " + hourMinSec
    elif re.search("\d{4}-\d{2}-\d{2}", str(date)) is not None:
        #splitDate = [each.strip() for each in date.split('.')]
        #print(splitDate)
        #splitDateLen = len(splitDate)
        #if splitDateLen == 2:
        result = str(date).split('.')[0]
        #else:
            #print(splitDate)
            #result = date
    elif len(str(date)) <= 8 and re.search("UTC", date) is None: # time_offset / longest_idle_time(-1 일때 처리) / active_time(0 일때 처리) / run_time / other_time / bed_time / sleep_time / wake_up_time / stand_time / others_time / walk_time / longest_active_time / duration /stand_time
        if not math.isnan(float(date)):
            result = convertMillis(int(float(date)))
    elif len(str(date)) == 13: # 13 digits unixtime / day_time / set_time / start_date / date / update_time / create_time / end_time / start_time / start_date / last_sync_time
        result = datetime.fromtimestamp(int(date)/1000).strftime("%Y-%m-%d %H:%M:%S")
    else: # UTC+0900. time_offset
        result = date
                   
    return result


# ## 2-3. 최신 데이터만 가져오는 함수(이전 파일 마지막 create_time, table이름 리턴)

# In[4]:


# 최신 파일만 가져오기 위해 이전 파일에서 마지막 create_time을 찾아서 리턴, DB에 전송하기 위해 테이블 이름도 함께 리턴
def findBeforeLastTime(eachCsv):
    # 해당 파일의 이전 파일을 찾는다. (인덱스로 찾으면 정확히 매칭이 되지 않음)
    # 1. 해당 파일의 이름을 추출
    fileName = eachCsv.split("/")[-1].split(".")
    del fileName[-2:]
    fileName = ".".join(fileName)
    
    # 기타) DB에 전송하기 위해 테이블 이름 추출
    tableName = fileName.split(".")[-1]
 
    # 2. 해당 파일 이름을 이전 디렉토리 경로와 합친다
    fileStartName = os.path.join(usersBeforePath[idx],fileName)

    # 3. 위에서 정제한 fileStartName으로 시작되고, .csv로 끝나는 파일을 찾는다
    try :
        beforeFileDir = glob('{}*.csv'.format(fileStartName)).pop()   # 리스트로 담기기 때문에 pop을 써서 str로 담아준다.
    except Exception as e:
        return "0", tableName
        print(e)
        
    # 4. CSV 파일 읽어오기  (나중에 숫자를 idx로 바꾸기)
    beforeHealthDF = pd.read_csv(beforeFileDir, skiprows=1, index_col=False)

    # 5 컬럼헤더 정제
    columnsList = beforeHealthDF.columns.tolist()   # 컬럼헤더를 리스트로 바꾼다
    refinedColumnList = splitColumn(columnsList)  # com.~~을 정제하는 함수 로직 실행
    beforeHealthDF.columns = refinedColumnList      # 정제된 리스트를 다시 컬럼헤더로

    # 6 2007. 02. 03 형식 또는 timestamp를 2007-02-03 형식으로 정제
    columns = beforeHealthDF.columns.values
    targetColumns = targetTimeCol(columns)

    for each in targetColumns:
        beforeHealthDF[each] = beforeHealthDF[each].apply(dateTodatetime)

    # 이전 파일에서 마지막 시간을 추출
    beforeLastTime = beforeHealthDF.create_time.max()
    
    return beforeLastTime, tableName


# ## 2-4. 데이터 베이스 이관 함수

# In[5]:


## 기존 데이터베이스 테이블에 없는 컬럼값을 입력했을 때 발생되는 에러를 반영하여 데이터베이스 테이블에 컬럼을 추가하는 함수
def alterColumnToDB(error, tableName, config):
    try:
        conn = MySQLdb.connect(**config)
        cur = conn.cursor()
        query = ""
        if re.search("1054", error) is not None:
            column = "".join(re.findall("\w", error.split(' ')[4]))
            query = "alter table {0} add column {1} text".format(tableName, column)
            cur.execute(query)
        elif re.search("1366", error) is not None:
            column = error.split(" ")[8].split("`")[-2]
            query = "alter table {0} modify column {1} text".format(tableName, column)
            cur.execute(query)
        elif re.search("1265", error) is not None:
            column = error.split(" ")[6].split("'")[1]
            query = "alter table {0} modify column {1} mediumtext".format(tableName, column)
            cur.execute(query)
        conn.close()
    except Exception as e:
        print(e)
            
## 데이터베이스 테이블에 데이터를 추가하는 함수
def dataToDB(engineInfo, recentHealthDF, tableName):
    error = ""
    try:
        engine = create_engine(engineInfo)
#         engine = create_engine("mysql+pymysql://root:1234@13.125.210.149:3306/health")
        recentHealthDF.to_sql(name="{}".format(tableName), con=engine, if_exists="append", index=False)
#         recentHealthDF.to_sql(name="{}".format(tableName), con=engine, if_exists="replace", index=False)
    except Exception as e:
        print(e)
        error = str(e)
        print("failed to transfer healthData to DB")
        
        if re.search("(1054|1366|1265)", error) is not None:
            alterColumnToDB(error, tableName, config)
            dataToDB(engineInfo, recentHealthDF, tableName)

# In[ ]:





# # 3. 실행 로직

# ## 3-1. 전역변수 설정

# In[6]:

# 1.1 데이터베이스 관련 전역변수. create_engine / MySQLdb.connect 시 사용
db_name = db_login['db_name']
db_api_name = db_login['db_api_name']
db_user = db_login['db_user']
db_password = db_login['db_password']
db_host = db_login['db_host']
db_port = db_login['db_port']
db_schema = db_login['db_schema']

engineInfo = "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(db_name, db_api_name, db_user, db_password, db_host, db_port, db_schema)
#print(engineInfo)
config = {"user":db_user, "password":db_password, "host":db_host, "port":db_port, "db":db_schema}
#print(config)

# 1.2 기본 디렉토리 설정
engine = create_engine(engineInfo)
query = "select * from meta_variables_dir"
variables = pd.read_sql(query, engine)

basedir = variables.basedir.values[0]
# print(basedir)

# 1.3 userID와 매칭시키기 위한 ID 데이터 딕셔너리로 설정 (최종적으로는 웹 로그인 시 세션에서 ID를 받아와야 함)
userIDDic = {"shinee" : "shinee", "donghue" : "dong2", "hoseong" : "hocastle"}


# # 3-2. 로직에 사용할 유저별 디렉토리 리스트화

# In[7]:


# 2.1 유저별 디렉토리 리스트
usersDirList = findTreeDir(basedir)

# 2.2 유저별 마지막 날짜의 디렉토리 리스트 (usersDirList의 하위 디렉토리를 리스트로 추출)
usersLatestPath = findLatest(usersDirList, 1)

# 3.1 유저별 마지막 날짜 이전의 디렉토리 리스트 (각 유저의 최신 데이터를 구별하기 위해 이전 날짜의 하위 디렉토리를 찾는다)
usersBeforePath = findLatest(usersDirList, 2)


# ## 3-3. CSV 파일을 읽어 데이터를 정제하고, 이전 파일과 비교해 최신 데이터만 DB에 보내는 함수

# In[22]:


for idx, val in enumerate(usersLatestPath):
    # 3.2 각 사람의 마지막 csv 파일 경로를 읽어온다
    eachCsvPath = findCsvDir(val)

    # DB에 넣을 때 ID컬럼에 값을 추가하기 위한 로직 (최종적으로는 웹 로그인 시 세션에서 ID를 받아와야 함)
    userName = val.split("/")[2]
    for eachCsv in eachCsvPath:
        #print(eachCsv)   # 디버깅용
        # 3.3 CSV 파일 읽어오기
        eachHealthDF = pd.read_csv(eachCsv, skiprows=1, index_col=False)
        
        # 3.4 컬럼헤더 정제
        columnsList = eachHealthDF.columns.tolist()   # 컬럼헤더를 리스트로 바꾼다
        refinedColumnList = splitColumn(columnsList)  # com.~~을 정제하는 함수 로직 실행
        eachHealthDF.columns = refinedColumnList      # 정제된 리스트를 다시 컬럼헤더로
        
        # 3.4 2007. 02. 03 형식 또는 timestamp를 2007-02-03 형식으로 정제
        columns = eachHealthDF.columns.values
        targetColumns = targetTimeCol(columns)

        for each in targetColumns:
            eachHealthDF[each] = eachHealthDF[each].apply(dateTodatetime)
        
        # 3.5 최신 파일 처리
        beforeLastTime, tableName = findBeforeLastTime(eachCsv)
        
        sortKey = ['create_time']
        eachLastTime = eachHealthDF.create_time.max()
        
        if eachLastTime == beforeLastTime:
            recentHealthDF = eachHealthDF
        else:
            recentHealthDF = eachHealthDF.loc[eachHealthDF.create_time > beforeLastTime].sort_values(by=sortKey)
#         recentHealthDF = eachHealthDF if eachLastTime == beforeLastTime else eachHealthDF.loc[eachLastTime > beforeLastTime].sort_values(by=sortKey)
        
        # 3.6 ID 컬럼과 ID 값 추가
        recentHealthDF['id'] = userIDDic[userName]
        

        # 3.7 DB에 데이터 전송
        dataToDB(engineInfo, recentHealthDF, tableName)
       
        time.sleep(1)
