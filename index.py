## 네이버 nba 플레이오프 경기기록 가져오기
import requests
from bs4 import BeautifulSoup
# URL
req = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blkw&qvt=0&query=2020-2021%20%EB%AF%B8%EA%B5%AD%ED%94%84%EB%A1%9C%EB%86%8D%EA%B5%AC%20%EC%BB%A8%ED%8D%BC%EB%9F%B0%EC%8A%A4%20%EC%A4%80%EA%B2%B0%EC%8A%B9')
# html src 가져오기
html = req.text

soup = BeautifulSoup(html, 'html.parser')

team_Title = soup.select(
    '#_calLayerBaseSportsDbSearch > div.api_cs_wrap._cs_nba > div:nth-child(4) > div > div.tmp_area._el_scroll > table > tbody > tr > td.score > a > em'
)
titleLst = []

for j in team_Title:
    titleLst.append(j.text)
with open('result.txt', 'w') as f :
    pass
for i in range(len(titleLst)):
    with open('result.txt', 'a') as f :
        f.write(titleLst[i]+" ")
        if i % 3 == 2 : f.write('\n')
result = ''
with open('result.txt', 'r') as f1:
    for k in f1.readlines():
        result += k


import os
import smtplib
# 이메일 메시지에 다양한 형식을 중첩하여 담기 위한 객체
from email.mime.multipart import MIMEMultipart

# 이메일 메시지를 이진 데이터로 바꿔주는 인코더
from email import encoders

# 텍스트 형식
from email.mime.text import MIMEText

# MIMEBase(_maintype, _subtype)
# MIMEBase(<메인 타입>, <서브 타입>)
from email.mime.base import MIMEBase

smtp_info = dict({"smtp_server" : "smtp.naver.com", # SMTP 서버 주소
                  "smtp_user_id" : "아이디",
                  "smtp_user_pw" : "비번",
                  "smtp_port" : 587}) # SMTP 서버 포트

# 메일 내용 작성
title = "메일 제목"
content = result
sender = smtp_info['smtp_user_id'] # 송신자(sender) 메일 계정
receiver = "수신자아이디"

# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg = MIMEText(_text = content, _charset = "utf-8") # 메일 내용

msg['Subject'] = title # 메일 제목
msg['From'] = sender # 송신자
msg['To'] = receiver # 수신자

def send_email(smtp_info, msg):
    with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
        # TLS 보안 연결
        server.starttls()
        # 로그인
        server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])

        # 로그인 된 서버에 이메일 전송
        response = server.sendmail(msg['from'], msg['to'], msg.as_string()) # 메시지를 보낼때는 .as_string() 메소드를 사용해서 문자열로 바꿔줍니다.

        # 이메일을 성공적으로 보내면 결과는 {}
        if not response:
            print('이메일을 성공적으로 보냈습니다.')
        else:
            print(response)

def make_multimsg(msg_dict):
    multi = MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        # 각 타입에 적절한 MIMExxx() 함수를 호출하여 msg 객체를 생성한다.
        if key == 'text':
            with open(value['filename'], encoding='utf-8') as fp:
                msg = MIMEText(fp.read(), _subtype=value['subtype'])
        else:
            with open(value['filename'], 'rb') as fp:
                msg = MIMEBase(value['maintype'], _subtype=value['subtype'])
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
        # 파일 이름을 첨부파일 제목으로 추가
        msg.add_header('Content-Disposition', 'attachment',filename=os.path.basename(value['filename']))

        # 첨부파일 추가
        multi.attach(msg)

    return multi


send_email(smtp_info, msg)