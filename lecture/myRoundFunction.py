#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 함수 설명 :
# 정수, 실수에 관계 없이 모든 수의 반올림, 올림, 내림을 계산할 수 있다.

# 자리수는 파이썬의 인덱스 방식을 따른다.
# 소수점 1, 2, 3 번째 자리는 num_digits에 1, 2, 3을 넣으면 되고,
# 정수 일, 십, 백 번째 자리는 마이너스 인덱스 방식으로 num_digits에 -1, -2, -3을 넣으면 된다.


# ### 반올림 함수

# In[5]:


def roundFunction(number,num_digits):
    # step1: 입력값(inValue)에 반올림 해서 최종적으로 표시할 소숫점 자릿수(decimalPlace)를 곱한다.
    # 일, 십, 백의자리수까지 나타내려면 num_digits에 -1, -2, -3을 넣으면 된다.
    step1 = number * (10 ** num_digits)
    # step2: step1 결과에 0.5를 더한 후 int로 캐스팅한다.
    step2 = int(step1 + 0.5)
    # step3: step2 결과를 step1에서 곱한 자릿수만큼 나눈다.
    step3 = step2 / (10 ** num_digits)
    return step3


# ### 올림 함수

# In[6]:


def roundUpFunction(number,num_digits):
    # step1: 입력값(inValue)에 올림 해서 최종적으로 표시할 소숫점 자릿수(decimalPlace)를 곱한다.
    # 일, 십, 백의자리수까지 나타내려면 num_digits에 -1, -2, -3을 넣으면 된다.
    step1 = number * (10 ** num_digits)
    # step2: step1 결과에 0.9를 더한 후 int로 캐스팅한다.
    step2 = int(step1 + 1)
    # step3: step2 결과를 step1에서 곱한 자릿수만큼 나눈다.
    step3 = step2 / (10 ** num_digits)
    return step3


# ### 내림 함수

# In[7]:


def roundDownFunction(number,num_digits):
    # step1: 입력값(inValue)에 내림 해서 최종적으로 표시할 소숫점 자릿수(decimalPlace)를 곱한다.
    # 일, 십, 백의자리수까지 나타내려면 num_digits에 -1, -2, -3을 넣으면 된다.
    step1 = number * (10 ** num_digits)
    # step2: step1 결과에 int 캐스팅한다.
    step2 = int(step1)
    # step3: step2 결과를 step1에서 곱한 자릿수만큼 나눈다.
    step3 = step2 / (10 ** num_digits)
    return step3

