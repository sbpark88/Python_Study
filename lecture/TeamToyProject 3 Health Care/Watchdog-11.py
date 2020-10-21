#!/usr/bin/env python
# coding: utf-8

# In[90]:


import os, re
from glob import glob
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
        csvList = [file for file in fileList if (file.endswith(".csv"))                    and (file.split("\\")[-1].split(".")[0] == "com")                    and (re.search("(food|breath|reward|hist|recommend)", file) is None)]
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
    
class Target: 
    #watchDir에 감시하려는 디렉토리를 명시한다.
    def __init__(self, baseDir):
        self.observer = Observer()   #observer객체를 만듦
        self.usersDirList = findCsvDir(baseDir)
        self.watchDir = self.usersDirList
        
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        print(event)

    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(event)

if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
    baseDir = "./HealthCare/"
    w = Target(baseDir)
    w.run()

