#!/usr/bin/env python
# coding: utf-8

# # DB 접속 엔진 관련 (v1.0.1 updated 20.05.05)

# In[1]:


def PrintDbEngine() :
    db = []
    db.append('import psycopg2                          # PostgreSQL을 사용 가능하게 해준다.')
    db.append('import pymysql                           # MariaDB를 사용 가능하게 해준다.')
    db.append('from sqlalchemy import create_engine     # DB 접속 엔진을 만들어준다.')
    db.append('\n# AWS PostgreSQL 데이터베이스 접속 엔진 생성.')
    db.append("aws_postgresql_url = 'postgresql://haiteam:haiteam@www.hadoopkorea.com:5432/postgres'")
    db.append('engine_postgresql = create_engine(aws_postgresql_url)')
    db.append('\n# AWS MariaDB 데이터베이스 접속 엔진 생성.')
    db.append("aws_mariadb_url = 'mysql+pymysql://kopo:kopo@www.hadoopkorea.com:3306/kopo'")
    db.append('engine_mariadb = create_engine(aws_mariadb_url)')

    for i in range(0,len(db)):
        print(db[i])


# In[2]:


# PrintDbEngine()    # 디버깅용.


# # 크롤링 관련

# In[3]:


def PrintWebCrawling() :
    crawling = []
    crawling.append('import requests, bs4')
    crawling.append('from selenium import webdriver')
    crawling.append('from selenium.webdriver.common.keys import Keys')
    crawling.append('driver_loc = "/Applications/chromedriver"\n')
    crawling.append('options = webdriver.ChromeOptions()')
    crawling.append('options.add_argument("window-size=1920x1080")              # 대부분은 적용이 안 되는 것 같다.')
    crawling.append("options.add_argument('headless')                           # 리눅스처럼 웹 화면 없는 경우에도 실행 가능.")
    crawling.append("options.add_argument('disable-gpu')")
    crawling.append('driver = webdriver.Chrome(driver_loc, options=options)')
    crawling.append('driver.maximize_window()                                   # 이렇게 해주면 무조건 최대화 시킨다. 위에 픽셀보다 잘 먹힘.')
    crawling.append('driver.implicitly_wait(3)                                  # 웹페이지 파싱 될 때까지 최대 3초 기다려줌.')
    crawling.append('')
    crawling.append('from selenium.webdriver.common.action_chains import ActionChains')
    crawling.append('import time')
    crawling.append('from selenium.webdriver.support import expected_conditions as EC')
    crawling.append('from selenium.webdriver.common.by import By')
    crawling.append('from selenium.webdriver.support.ui import WebDriverWait as wait')
    crawling.append('')
    crawling.append('from pandas.io.json import json_normalize                  # 그냥 pd.json_normalize를 사용하자.')
    crawling.append('from lxml import html')
    crawling.append('from urllib.request import Request, urlopen')
    crawling.append('from urllib.parse import urlencode, quote_plus, unquote')
    
    for i in range(0,len(crawling)):
        print(crawling[i])


# In[4]:


# PrintWebCrawling()    # 디버깅용.


# # 이메일 발송 관련

# In[5]:


def PrintEmail() :
    email = []
    email.append('import smtplib                            # SMTP 프로토콜 로드')
    email.append('from email.message import EmailMessage    # 이메일을 간단하게 보낼수 있는 라이브러리 로드')
    email.append('import getpass')
    email.append('import pickle                             # 파이썬에 있는 자료를 저장하고 내보내고 하게 해줌.')
    
    for i in range(0,len(email)):
        print(email[i])


# In[6]:


# PrintEmail()    # 디버깅용.

