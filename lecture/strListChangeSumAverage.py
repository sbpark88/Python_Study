#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 리스트 내의 숫자를 정수형, 실수형, 문자형으로 자유롭게 바꿀 수 있다.
# 또한 문자형으로 된 리스트의 합, 평균을 구할 수 있다.


# In[ ]:


# 숫자로 구성된 리스트를 문자로 바꾸는 함수.
def numberToString(inputList):
    for i in range(0,len(inputList),):
        inputList[i] = str(inputList[i])
    return inputList


# In[ ]:


# 문자로 구성된 리스트를 정수로 바꾸는 함수.
def stringToInt(inputList):
    for i in range(0,len(inputList),):
        inputList[i] = int(inputList[i])
    return inputList


# In[ ]:


# 문자로 구성된 리스트를 실수로 바꾸는 함수.
def stringToFloat(inputList):
    for i in range(0,len(inputList),):
        inputList[i] = float(inputList[i])
    return inputList


# In[ ]:


# 문자로 구성된 리스트의 합을 구하는 함수.
def stringNumberSum(inputList):
    for i in range(0,len(inputList),):
        inputList[i] = int(inputList[i])
    return sum(inputList)


# In[ ]:


# 문자로 구성된 리스트의 평균을 구하는 함수.
def stringNumberAvg(inputList):
    for i in range(0,len(inputList),):
        inputList[i] = int(inputList[i])
    return sum(inputList) / len(inputList)

