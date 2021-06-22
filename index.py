## parser.py
import requests
from bs4 import BeautifulSoup
import json
import os

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blkw&qvt=0&query=2020-2021%20%EB%AF%B8%EA%B5%AD%ED%94%84%EB%A1%9C%EB%86%8D%EA%B5%AC%20%EC%BB%A8%ED%8D%BC%EB%9F%B0%EC%8A%A4%20%EC%A4%80%EA%B2%B0%EC%8A%B9')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    '#_calLayerBaseSportsDbSearch > div.api_cs_wrap._cs_nba > div:nth-child(4) > div > div.tmp_area._el_scroll > table > tbody > tr > .score span'
    )

data = []
print(my_titles)

for title in my_titles:
    data.append(title)

print(data)
# with open('result.txt', 'a') as f :
#     f.write(data)