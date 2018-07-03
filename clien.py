#!/usr/bin/env python
import urllib3

import requests
from bs4 import BeautifulSoup as Soup
import sys
from urllib import request
import getpass
import os
import readline
import json
from PIL import Image
import urllib.request
import webbrowser
import pickle


#!/usr/bin/env python
# requests_ssl.py
# main script

import requests
import os
import sys
import certifi
import time

import os
global path
path = os.path.dirname(os.path.realpath(__file__))

try:
    print("최신 버전이 있을 경우 clienBBS 를 최신으로 업데이트 합니다.")
    print("업데이트 된 버전은 다음 실행부터 적용됩니다.")
    os.system('pip install clienBBS --upgrade >> pip.log ')
    os.system('pip3 install clienBBS --upgrade >> pip.log ')
except:
    pass

def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                        relative)

cert_path = resource_path(certifi.where())

login_url = 'https://www.clien.net/service/login'

#functions
def set_csrf(page, param):
    html = page.text
    soup = Soup(html, 'html.parser')
    csrf = soup.find('input', {'name': '_csrf'})
    return {**param, **{'_csrf': csrf['value']}}


park_url = "https://www.clien.net/service/board/park?&od=T31&po="
news_url = "https://www.clien.net/service/board/news?&od=T31&po="
tips_url = "https://www.clien.net/service/board/lecture?&od=T31&po="
jirum_url = "https://www.clien.net/service/board/jirum?&od=T31&po="
use_url = "https://www.clien.net/service/board/use?&od=T31&po="
buysell_url = "https://www.clien.net/service/board/sold?&od=T31&po="
qna_url = "https://www.clien.net/service/board/kin?&od=T31&po="
useful_url = "https://www.clien.net/service/board/useful?&od=T31&po="
base_url = "https://www.clien.net"

global bbs_title
global bbs
global login_session
global logged_in_user
global keyword
global read_log

try:
    with open(os.path.join(path,'read_log.pkl'),'rb') as fin:
        read_log = pickle.load(fin)    
except:
    read_log = {}

login_session = None
logged_in_user = None
bbs = None    

import sys
import socket
import select
import readline

def chat_client():
    global login_session
    global logged_in_user
    if login_session is None:
        print("\n채팅에 참여 하시려면 로그인 하셔야 합니다.")
        login_session = login()
    
    if login_session is None:
        input('로그인 하시지 않으면 대화에 참여하실 수 없습니다. (엔터) 계속')
        return

    nick = input("\n채팅에 사용할 별명을 입력하세요: ")
    host = '45.55.183.136'
    port = 9009
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('clienBBS의 채팅 서버가 준비되지 않은 상태입니다.')
        print('잠시 후 다시 시도해 보세요')
        cm = input("(엔터) 계속 .. ")
        return
     
    print('서버에 접속하였습니다. 즐거운 시간 되세요..\n')
    print('대화를 마치시려면 **를 입력하세요. **who 를 입력하시면 현재 참여 인원을 보실 수 있습니다. \n')
    
    msg = bytes('**cmd**:enter:'+nick+' ('+logged_in_user+')',"utf-8")
    s.send(msg)

    sys.stdout.write('['+nick+'('+logged_in_user+')] '); sys.stdout.flush()

    while 1:
        
        socket_list = [sys.stdin, s]
        
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        erase = '\x1b[1A\x1b[2K'
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                data = data.decode("utf-8")
                if not data :
                    print('\nDisconnected from chat server')
                    return
                else :
                    print(erase)
                    sys.stdout.write(data.strip()+"\n\n["+nick+' ('+logged_in_user+')] ')
                    sys.stdout.flush()          
            else :
                msg = input("")
                
                if msg.strip()=="**who":
                    print("**who 받음")
                    msg = bytes("**cmd**:who:","utf-8")
                    s.send(msg)

                elif msg.strip()=="**":
                    print(" 안녕히 계세요 ")
                    msg = bytes('**cmd**:quit:'+nick+' ('+logged_in_user+')',"utf-8")
                    s.send(msg)
                    return
                else:
                    print(erase)

                    msg = bytes('['+nick+' ('+logged_in_user+')] '+msg,"utf-8")
                    s.send(msg)
                    time.sleep(1)
                    sys.stdout.write('['+nick+' ('+logged_in_user+')] '); sys.stdout.flush() 


def display_img(img):
    if img is not None:
        with urllib.request.urlopen(img) as url:
            with open('temp.tmp', 'wb') as f:
                f.write(url.read())
        img = Image.open('temp.tmp')
        img.show()

		
def welcome():
    global login_session
    global read_log
    global path
    clear_screen()
    welcome_msg = """
클리앙에 오신 것을 환영합니다.
__________________________________________________________________________________________________________________________________________
 __    __    ___  _         __   ___   ___ ___    ___      ______   ___      
|  T__T  T  /  _]| T       /  ] /   \ |   T   T  /  _]    |      T /   \     
|  |  |  | /  [_ | |      /  / Y     Y| _   _ | /  [_     |      |Y     Y    
|  |  |  |Y    _]| l___  /  /  |  O  ||  \_/  |Y    _]    l_j  l_j|  O  |    
l  `  '  !|   [_ |     T/   \_ |     ||   |   ||   [_       |  |  |     |    
 \      / |     T|     |\     |l     !|   |   ||     T      |  |  l     !    
  \_/\_/  l_____jl_____j \____j \___/ l___j___jl_____j      l__j   \___/     
                                                                             
    __  _      ____    ___  ____       ____     ___  ______                  
   /  ]| T    l    j  /  _]|    \     |    \   /  _]|      T                 
  /  / | |     |  T  /  [_ |  _  Y    |  _  Y /  [_ |      |                 
 /  /  | l___  |  | Y    _]|  |  |    |  |  |Y    _]l_j  l_j                 
/   \_ |     T |  | |   [_ |  |  | __ |  |  ||   [_   |  |                   
\     ||     | j  l |     T|  |  ||  T|  |  ||     T  |  |                   
 \____jl_____j|____jl_____jl__j__jl__jl__j__jl_____j  l__j                 
                                                                             
 ______    ___  ____   ___ ___  ____  ____    ____  _                        
|      T  /  _]|    \ |   T   Tl    j|    \  /    T| T                       
|      | /  [_ |  D  )| _   _ | |  T |  _  YY  o  || |                       
l_j  l_jY    _]|    / |  \_/  | |  | |  |  ||     || l___                    
  |  |  |   [_ |    \ |   |   | |  | |  |  ||  _  ||     T                   
  |  |  |     T|  .  Y|   |   | j  l |  |  ||  |  ||     |                   
  l__j  l_____jl__j\_jl___j___j|____jl__j__jl__j__jl_____j   (clienBBS)  

  VER 0.50 1/5/2017)

  [공지] OSX의 QuickLook 사용이 편리하도록 첨부된 사진,영상의 링크를 글에 표시하였습니다.
  버그 알림 및 문의는 Matt Lee (johnleespapa@gmail.com, 인스타그램 @papamattlee)
  [보다 쾌적한 사용을 위해 터미널의 상하,좌우폭을 조절해주세요]
__________________________________________________________________________________________________________________________________________

  """
    print(welcome_msg)
    while True:
        cmd_list="(l) 로그인 (엔터) 게스트로 시작 (\q) 종료하기 >> "
        cmd = input(cmd_list)
        if cmd.strip()=="":
            break
        if cmd.strip()=="\q":
            print("")
            print("안녕히 가십시오. ")
            print("")
            
            with open(os.path.join(path,'read_log.pkl'),'wb') as fout:
                pickle.dump(read_log, fout)
            sys.exit()
        if cmd.strip()=="l":
            login_session = login()
            if login_session is not None:
                break

def show_top_menu():
    global logged_in_user

    clear_screen()
    welcome_msg = """__________________________________________________________________________________________________________________________________________
    __  _      ____    ___  ____       ____     ___  ______                  
   /  ]| T    l    j  /  _]|    \     |    \   /  _]|      T                 
  /  / | |     |  T  /  [_ |  _  Y    |  _  Y /  [_ |      |                 
 /  /  | l___  |  | Y    _]|  |  |    |  |  |Y    _]l_j  l_j                 
/   \_ |     T |  | |   [_ |  |  | __ |  |  ||   [_   |  |                   
\     ||     | j  l |     T|  |  ||  T|  |  ||     T  |  |                   
 \____jl_____j|____jl_____jl__j__jl__jl__j__jl_____j  l__j                   
                                                                             
 ______    ___  ____   ___ ___  ____  ____    ____  _                        
|      T  /  _]|    \ |   T   Tl    j|    \  /    T| T                       
|      | /  [_ |  D  )| _   _ | |  T |  _  YY  o  || |                       
l_j  l_jY    _]|    / |  \_/  | |  | |  |  ||     || l___                    
  |  |  |   [_ |    \ |   |   | |  | |  |  ||  _  ||     T                   
  |  |  |     T|  .  Y|   |   | j  l |  |  ||  |  ||     |                   
  l__j  l_____jl__j\_jl___j___j|____jl__j__jl__j__jl_____j     

* 재미있게 사용하셨다면 유튜브 '이씨네 미국살이 (https://goo.gl/FbhCa7)' 를 방문해주세요.
* 인스타그램 @papamattlee 를 팔로우해주세요

열람하실 게시판을 선택해 주세요.

 (f) 모두의 공원	(u) 사용기
 (n) 새소식		(s) 회원중고장터
 (l) 팁/강좌		(q) 아무거나 질문
 (j) 알뜰 구매		(t) 유용한 사이트
__________________________________________________________________________________________________________________________________________

  """
    if logged_in_user is not None:
        print(logged_in_user+" 님 반갑습니다.")
    print(welcome_msg)
# -*- coding: utf8 -*-

import re

def length_kor(text):
    text = text.replace("—","-")
    try:
        length = len(text.encode('euc-kr'))
    except:
        length = len(text)
    return length

def clear_screen():
    print(chr(27) + "[2J")

def show_header():
    clear_screen()
    global logged_in_user
    if logged_in_user is not None:
        print(logged_in_user+" 님 반갑습니다.")
    print("""
    __  _      ____    ___  ____       ____     ___  ______                  
   /  ]| T    l    j  /  _]|    \     |    \   /  _]|      T                 
  /  / | |     |  T  /  [_ |  _  Y    |  _  Y /  [_ |      |                 
 /  /  | l___  |  | Y    _]|  |  |    |  |  |Y    _]l_j  l_j                 
/   \_ |     T |  | |   [_ |  |  | __ |  |  ||   [_   |  |                   
\     ||     | j  l |     T|  |  ||  T|  |  ||     T  |  |                   
 \____jl_____j|____jl_____jl__j__jl__jl__j__jl_____j  l__j   
 
  재미있게 사용하셨다면 유튜브 '이씨네 미국살이 (https://goo.gl/FbhCa7)' 를 방문해주세요.
  인스타그램 @papamattlee 를 팔로우해주세요
 """)
def show_lower():
    print("__________________________________________________________________________________________________________________________________________")    

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text).replace("&nbsp;","")

def reply(bbs_title, article_num, article_data, sub_page):
    global login_session
    global bbs
    #page_data = Soup(login_session.get(base_url).text, 'lxml')
    #if "나의글"in page_data.text:
    #    print ('로그인에 성공 하였습니다.')

    if login_session is None:
        print("댓글을 다시려면 로그인 하셔야 합니다.")
        login_session = login()
    
    if login_session is None:
        input('로그인 하시지 않으면 댓글을 달 수 없습니다. (엔터) 계속')
        return
    else:
        article_url = base_url+article_data[sub_page*20+article_num][2]
        article_id = article_url.split("https://www.clien.net/service/")[1].split("?")[0]
        comment_url = "https://www.clien.net/service/api/"+article_url.split("https://www.clien.net/service/")[1].split("?")[0]+"/comment/regist"
        lines = []
        print("내용 입력을 마치시리면 \d 후 엔터를 입력해주세요. 글 작성 취소는 \c를 입력하세요 ")
        idx = 0
        while True:
            line = input(" "+str(idx)+": ")
            idx+=1
            if line=="\d":
                break
            if line=="\c":
                input("글 쓰기를 취소합니다 (엔터) ")
                return
            else:
                lines.append(line)
        lines.append("<br> - clienBBS 로 작성한 댓글입니다.")
        content = ""
        for line in lines:
            if line.strip()=="":
                line="<br>"
            content+="<p>"+line+"</p>"

        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        
        data = {
                    'boardSn': article_id.split("/")[-1],
                    'param': "{\"comment\":\"<p>"+content+"</p>\",\"images\":[]}"
                }
        main_page = login_session.get(article_url)
        data = set_csrf(main_page, data)
        headers['X-CSRF-TOKEN'] = data['_csrf']
        data = json.loads(json.dumps(data))
        regist_req = login_session.post(comment_url, data=data)
        if regist_req.status_code != 200:
            print ('댓글이 달리지 않았습니다.')
        else:
            print ('댓글이 달렸습니다.')

def write(bbs_title):
    global login_session
    
    if login_session is None:
        print("글을 쓰시려면 로그인 하셔야 합니다.")
        login_session = login()
    
    if login_session is None:
        input('로그인 하시지 않으면 글을 쓰실 수 없습니다. (엔터) 계속')
        return
    else:
        print("")
        title = input("제목을 입력하세요 > ")
        print("")
        lines = []
        print("내용 입력을 마치시리면 \d 후 엔터를 입력해주세요. 글 작성 취소는 \c를 입력하세요 ")
        idx = 0
        while True:
            line = input(" "+str(idx)+": ")
            idx+=1
            if line=="\d":
                break
            if line=="\c":
                input("글 쓰기를 취소합니다 (엔터) ")
                return
            else:
                lines.append(line)
        lines.append("<br> - clienBBS 로 작성한 글입니다.")
        content = ""
        for line in lines:
            if line.strip()=="":
                line="<br>"
            content+="<p>"+line+"</p>"
        
        params ="{\"commentAlarmYn\": true, \"content\": \""+content+"\", \"files\": [], \"images\": [], \"imageLocation\": \"IN\", \"htmlYn\": true, \"subject\": \""+title+"\", \"ccl\": \"\", \"source\": \"\"}"
        data = {
                    'mode':'regist',
                    'boardSn': '',
                    'param': params
                }
        params = json.loads(json.dumps(params))
        main_page = login_session.get(base_url)
        data = set_csrf(main_page, data)
        data = json.loads(json.dumps(data))
        #
        
        if bbs=="f":
            url = park_url
        
        if bbs =="n":
            url = news_url
        
        if bbs =="l":
            url = tips_url
        
        if bbs =="j":
            url = jirum_url
        
        if bbs =="u":
            url = use_url
        
        if bbs =="s":
            url = buysell_url
        
        if bbs =="q":
            url = qna_url
        
        if bbs =="t":
            url = useful_url

        api_url = "https://www.clien.net/service/api/"+url.split("https://www.clien.net/service/")[1].split("?")[0]
        
        proceed_yn = input("\n글을 등록 하시겠습니까? (네=Y,y,엔터)/(아니오=N,n)")
        if (proceed_yn=="" or proceed_yn.upper()=="Y") and len(title)>3 and len(content)>5 and title.strip()!="" and content.strip!="<p></p>":
            regist_req = login_session.post(api_url, data=data)
            if regist_req.status_code != 200:
                print ('새 글이 등록되지 않았습니다.')
            else:
                print ('새 글이 등록되었습니다.')
        else:
            print ('새 글이 등록되지 않았습니다.')

def open_web_page(url):
    webbrowser.open_new(url)

def show_comment(bbs_title, article_num, article_data, sub_page):
    article_url = base_url+article_data[sub_page*20+article_num][2]
    title = article_data[sub_page*20+article_num][0]
    author = article_data[sub_page*20+article_num][1]
    hits = article_data[sub_page*20+article_num][3]
    timestamp = article_data[sub_page*20+article_num][4]
    comment_url = "https://www.clien.net/service/"+article_url.split("https://www.clien.net/service/")[1].split("?")[0]+"/comment?order=date&po=0&ps=99999"
    comment_data = requests.get(comment_url,verify=cert_path).text
    comment_data_soup = Soup(comment_data, 'lxml')
    comment_row = comment_data_soup.findAll("div", {"data-role": "comment-row"})
    comment_json_list = []
    for item in comment_row:
        try:
            #print(item)
            comment = {}
            try:
                if "re" == item['class'][1]:
                    re_comment = True
                else:
                    re_comment = False
            except:
                re_comment =False
            comment['comment'] = item.find("div",{"class":"comment_content"}).find("div",{"class":"comment_view"}).text.strip()
            comment['username'] = item['data-author-id']
            comment['checkReComment'] = re_comment
            comment['commentSn'] = item['data-comment-sn']
            comment_json_list.append(comment)
        except:
            pass
    idx = 0
    clear_screen()
    show_header()
    print(bbs_title, "제목:'", title+"'", "글쓴이: ",author)
    print(" 총 "+ str(len(comment_json_list))+" 개의 댓글이 달렸습니다.")
    print("__________________________________________________________________________________________________________________________________________")
    print("")
    max_page = int((len(comment_json_list)/5))+1
    for i in range(0,((int(max_page) *5)-len(comment_json_list))):
        comment_json_list.append({})

    for page in range(0, int(max_page)):
        for item in comment_json_list[page*5:page*5+5]:
            try:
                comment = item['comment']
                username = item['username']
                re_comment_sn = item['checkReComment']
                comment_sn = item['commentSn']
                l = comment.replace("\n"," ").split(" ")
                n = 10
                lines = [' '.join(l[x:x+n]) for x in range(0, len(l), n)]
                idx = 0
                for line in lines:
                    line = remove_tags(line)
                    if idx==0:
                        line = "\""+line
                    if idx==len(lines)-1:
                        line = line+"\""
                    if re_comment_sn==True:
                        print("\t\t"+line.strip())
                    else:
                        print("\t"+line.strip())
                    idx+=1

                if re_comment_sn==True:
                    print("\t\t(by "+username+")")
                else:
                    print("\t(by "+username+")")
                print("")
            except:
                print("")
        if page!=max_page-1:
            print(" (계속 ...)")
        else:
            print(" -- 댓글의 마지막입니다. --")
            break
        print("__________________________________________________________________________________________________________________________________________")
        print("")
        cmd = input("PAGE:["+str(page+1)+"/"+str(max_page)+"] (엔터) 댓글 더 보기 (b,l) 뒤로가기/글목록 보기 (r) 댓글 달기 >> ")
        
        if cmd=="b" or cmd=="l":
            return
        
        if cmd=="r":
            reply(bbs_title, article_num, article_data, sub_page)
            show_comment(bbs_title, article_num, article_data, sub_page)

        clear_screen()
        show_header()
        print("__________________________________________________________________________________________________________________________________________")
        print("")

    show_lower()

    cmd = input("PAGE:["+str(page+1)+"/"+str(max_page)+"] (엔터) 글 목록 보기 (n) 다음 글 보기 (r) 댓글 달기>> ")

    if cmd=="r":
        reply(bbs_title, article_num, article_data, sub_page)
        show_comment(bbs_title, article_num, article_data, sub_page)
    
    elif cmd=="n":
        try:
            read_post(bbs_title, article_num+1, article_data, sub_page)
        except:
            input(" 다음 글이 없습니다. (엔터)")

def read_post(bbs_title, article_num, article_data, sub_page):
    article_url = base_url+article_data[sub_page*20+article_num][2]
    title = article_data[sub_page*20+article_num][0]
    author = article_data[sub_page*20+article_num][1]
    hits = article_data[sub_page*20+article_num][3]
    timestamp = article_data[sub_page*20+article_num][4]
    comment_no = article_data[sub_page*20+article_num][5]
    global read_log
    global path
    read_log[author.strip()+"_"+timestamp.strip()] = True
    board_type = article_url.split("/")[-2]
    
    if login_session != None and board_type == "sold":
        article_data_soup = Soup(login_session.get(article_url,verify=cert_path).text, 'lxml')
    else:
        article_data_soup = Soup(requests.get(article_url,verify=cert_path).text, 'lxml')
    
    post = article_data_soup.find("div", {"class": "post_content"}).text.strip()
    img = article_data_soup.find("div", {"class": "post_content"}).findAll("img")
    vid = article_data_soup.find("div", {"class": "post_content"}).findAll("iframe")

    if img is not None:
        for item in img:
            post = item['src']+"\n"+ post
    
    if vid is not None:
        for item in vid:
            post = item['src']+"\n"+ post
    
    if board_type == "sold":
        item_info = ""
        item_info+= "\n물품 정보"
        seller_info = article_data_soup.find("div", {"class": "market_product"})
        print(seller_info)
        items = seller_info.findAll("div",{"class":"product_table"})
        seller_contact = article_data_soup.find("table", {"class": "popup_contact"})
        for item in items:
            parsed_item = item.findAll("span")
            item_info+= parsed_item[0].text + " : " + parsed_item[1].text+"\n"
        
        if login_session != None and seller_contact != None:
            try:
                rows = seller_contact.find_all("tr")
                item_info+="\n판매자 정보"
                for row in rows:
                    item_info+=row.find("th").text + " : " + row.find("td").text +"\n"
            except:
                pass
        else:
            item_info+="\n판매자 정보는 가입 한 상태에서 15일이 지나야 볼 수 있습니다."
        item_info+="\n\n"
    post_lines = post.split("\n")
    new_post_lines = []
    for line in post_lines:
        l = line.split(" ")
        n = 10
        lines = [' '.join(l[x:x+n]) for x in range(0, len(l), n)]
        new_post_lines+=lines
    post_lines = new_post_lines

    max_page = (len(post_lines)/10)+1
    for i in range(0,((int(max_page) *10)-len(post_lines))):
        post_lines.append("\n")

    if board_type == "sold":
        start_page = -1
    else:
        start_page = 0
    for page in range(start_page, int(max_page)):
        clear_screen()
        show_header()
        print(bbs_title, "제목:'", title+"'", "글쓴이: ",author)
        print("__________________________________________________________________________________________________________________________________________")
        print("")
        

        if board_type == "sold" and page==-1:
            print(item_info)
        else:    
            for line in post_lines[page*10:page*10+10]:
                print(" "+line.strip()+"\n")
        if (page+1)!=int(max_page):
            print(" (계속...) ")
        else:
            if str(comment_no).strip()=="":
                print(" -- 글의 마지막입니다. --"+" 댓글이 없습니다")
            else:
                print(" -- 글의 마지막입니다. -- "+str(comment_no) + " 개의 댓글이 달렸습니다.")
        show_lower()
    
        if (page+1)!=int(max_page):
            cmd_list="[PAGE:"+str(page+1)+"/"+str(int(max_page))+"] (엔터) 다음 페이지 (i) 웹 브라우저에서 보기 (b) 뒤로 가기 (n) 다음글 읽기 (r) 댓글 달기 (\q) 종료 하기 >> "
        elif str(comment_no).strip()!="":
            cmd_list="[PAGE:"+str(page+1)+"/"+str(int(max_page))+"] (엔터) 댓글 보기 (i) 웹 브라우저에서 보기 (b) 뒤로가기 (n) 다음글 읽기(r) 댓글 달기 (\q) 종료 하기 >> "
        else:
            cmd_list="[PAGE:"+str(page+1)+"/"+str(int(max_page))+"] (엔터) 글 목록 보기 (i) 웹 브라우저에서 보기 (r) 댓글 달기 (n) 다음글 읽기 (\q) 종료 하기 >> "
        
        cmd = input(cmd_list)
        
        if (page+1)==int(max_page) and cmd.strip()=="" and str(comment_no).strip()!="":
            show_comment(bbs_title, article_num, article_data, sub_page)
    
        if cmd.strip()=="i":
            open_web_page(article_url)
            page = max_page - 1
            show_comment(bbs_title, article_num, article_data, sub_page)

        if cmd.strip()=="b":
            return
        
        if cmd.strip()=="n":
            try:
                read_post(bbs_title, article_num+1, article_data, sub_page)
            except:
                input(" 다음 글이 없습니다. (엔터)")

        if cmd.strip()=="\q":
            print("* 감사합니다. 안녕히가세요.")
            with open(os.path.join(path,'read_log.pkl'),'wb') as fout:
                pickle.dump(read_log, fout)
            sys.exit()
        
        if cmd.strip()=="r":
            reply(bbs_title, article_num, article_data, sub_page)
            show_comment(bbs_title, article_num, article_data, sub_page)
        
def get_list(bbs="f",page=0, keyword=None):
        global login_session
        data = []
        
        if bbs=="f":
            url = park_url
        
        if bbs =="n":
            url = news_url
        
        if bbs =="l":
            url = tips_url
        
        if bbs =="j":
            url = jirum_url
        
        if bbs =="u":
            url = use_url
        
        if bbs =="s":
            url = buysell_url
        
        if bbs =="q":
            url = qna_url

        if bbs =="t":
            url = useful_url
        
        if bbs =="f" or bbs == "n"  or bbs == "t":
            for page in (page*2,page*2+1):
                new_url = url+str(page)
                if keyword is not None:
                    new_url+="&sk=title&sv="+keyword
                    new_url="https://www.clien.net/service/search/board/"+new_url.split("board/")[1]

                if login_session is not None:
                    page_data = Soup(login_session.get(new_url, verify=cert_path).text, 'lxml')
                else:
                    page_data = Soup(requests.get(new_url, verify=cert_path).text, 'lxml')
                
                list_article = page_data.findAll("div", {"class": "list_item symph_row"})
                for item in list_article:
                    title = item.findAll("span")[2].text
                    try:
                        comment_no = item.findAll("span",{"class":"rSymph05"})[1].text
                    except:
                        comment_no = ""                    
                    hits = item.findAll("div")[3].span.text
                    link = item.find("a",{"class":"list_subject"})['href']
                    author = item['data-author-id'].strip()
                    timestamp = item.find("div",{"class":"list_time"}).span.span.text
                    data.append((title,author,link,hits,timestamp,comment_no))

        else:
            for page in (page*2,page*2+1):
                new_url = url+str(page)
                if keyword is not None:
                    new_url+="&sk=title&sv="+keyword
                    new_url="https://www.clien.net/service/search/board/"+new_url.split("board/")[1]
                if login_session is not None:
                    page_data = Soup(login_session.get(new_url, verify=cert_path).text, 'lxml')
                else:
                    page_data = Soup(requests.get(new_url, verify=cert_path).text, 'lxml')
                
                list_article = page_data.findAll("div", {"class": "list_item symph_row"})
                for item in list_article:
                    
                    try:
                        spans = item.find("div",{"class":"list_title"}).findAll("span")
                        for span in spans:
                            try:
                                span['class']
                            except:
                                title = span.text
                        
                    except:
                        title="PARSE ERROR"
                    
                    try:
                        comment_no = item.find("span",{"class":"rSymph05"}).text
                    except:
                        comment_no = ""

                    hits = item.findAll("div")[3].span.text
                    link = item.find("a",{"class":"list_subject"})['href']
                    author = item['data-author-id'].strip()
                    timestamp = item.find("div",{"class":"list_time"}).span.span.text
                    data.append((title,author,link,hits,timestamp,comment_no))
        return data


def login():
    global logged_in_user
    s = requests.Session()

    user_info = {}
    main_page = s.get(base_url)
    for i in range(0,3):  
        username = input('\n아이디: ')
        pswd = getpass.getpass('암호: ')
        user_info['userId'] = username
        user_info['userPassword'] = pswd
            
        user_info = set_csrf(main_page, user_info)
        login_req = s.post(login_url, data=user_info)
        
        if login_req.status_code != 200:
            print ('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
        else:
            page_data = Soup(s.get(base_url).text, 'lxml')
            if "나의글"in page_data.text:
                print ('로그인에 성공 하였습니다.')
                logged_in_user = user_info['userId']
                return s
            else:
                print ('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')

    print("로그인을 할수 없습니다. ")
    return None


def padding_str(text,len):
    padding_size = len-(length_kor(text))
    if padding_size>0:
        for i in range(0,padding_size):
            text+=" "
    text = text[:len]
    return text

def cmd_line():
    global read_log
    global path
    global login_session
    global bbs
    global bbs_title
    global keyword
    keyword = None
    article_data = []
    sub_page = 0
    page = 0
    while True:
        
        show_top_menu()
        cmd_list="(\q) 종료하기 >> "

        if len(article_data)==0:
            cmd = input(cmd_list)
            bbs = cmd.strip()
            
            #if cmd.strip()=="cc":
            #    chat_client()

            if cmd.strip()=="f":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [모두의 공원]"
            
            if cmd.strip()=="n":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [새소식]"

            if cmd.strip()=="l":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [팁/강좌]"

            if cmd.strip()=="j":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [알뜰 구매]"
            
            if cmd.strip()=="u":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [사용기]"
            
            if cmd.strip()=="s":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [회원 중고장터]"
            
            if cmd.strip()=="q":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [아무거나 질문]"

            if cmd.strip()=="t":
                page = 0
                keyword = None
                article_data = get_list(bbs=bbs,page=0,keyword=keyword)
                bbs_title = "* [유용한 사이트]"

            if cmd.strip()=="\q":
                print("안녕히 가십시오")
                with open(os.path.join(path,'read_log.pkl'),'wb') as fout:
                    pickle.dump(read_log, fout)
                sys.exit()
            if cmd.strip()=="\c":
                clear_screen()
            if cmd.strip()=="\l":
                pass
                #login_session = login()
        else:   
            idx = 0
            show_header()
            item_no = 0
            print(bbs_title)
            print("__________________________________________________________________________________________________________________________________________")
            
            for item in article_data[sub_page*20:]:
                title = padding_str(item[0],80)
                hits = padding_str(item[3],5)
                author = padding_str(item[1],10)
                timestamp = padding_str(item[4],10)       
                
                if item[5].strip()=="":
                    comment_no = padding_str(item[5],5)  
                else:
                    comment_no = padding_str("["+item[5]+"]",5)  
                
                try:
                    read_log[author.strip()+"_"+item[4].strip()]
                    print("  "+str(idx)+"\t"+title+" "+str(comment_no)+"\t by "+author+"\t"+timestamp+"\t"+hits)
                except:
                    print("* "+str(idx)+"\t"+title+" "+str(comment_no)+"\t by "+author+"\t"+timestamp+"\t"+hits)
                idx+=1
                if idx!=0 and idx%20==0:
                    break

            show_lower()
            cmd_list="[PAGE:"+str(page*3+sub_page)+"] (글번호) 글 읽기 (n)새글 확인 (t) 상위 메뉴 (s) 검색 (w) 글 쓰기 (\q) 종료 하기 (엔터) 다음 페이지 (b) 이전 페이지>> "
            cmd = input(cmd_list)
            
            try:
                article_num = int(cmd)
                if article_num>=0 and article_num<len(article_data):
                    cmd = "read"                    
            except:
                pass
            if cmd.strip()=="read":
                read_post(bbs_title, article_num, article_data, sub_page)
            
            if cmd=="s":
                
                if login_session is None:
                    print("\n글을 검색하시려면 로그인 하셔야 합니다.")
                    login_session = login()
                
                if login_session is None:
                    input('로그인 하시지 않으면 검색 하실 수 없습니다. (엔터) 계속')
                
                else:
                    keyword = input("\n검색어를 입력하세요 (빈 검색어=전체글 보기) >> ")
                    keyword = keyword.replace(" ","%20")
                    if keyword.strip()=="":
                        keyword = None

                    page = 0
                    sub_page = 0
                    article_data = get_list(bbs=bbs,page=page,keyword=keyword)

            if cmd=="w":
                write(bbs_title)
                page = 0
                sub_page = 0
                article_data = get_list(bbs=bbs,page=page,keyword=keyword)

            if cmd.strip()=="t":
                page = 0
                sub_page = 0
                article_data = []
            
            if cmd.strip()=="n":
                page = 0
                sub_page = 0
                article_data = get_list(bbs=bbs,page=page,keyword=keyword)
            
            if cmd.strip()=="b":
                if page==0 and sub_page==0:
                    input(" 더 이상 이전 페이지가 없습니다. >>")
                else:
                    sub_page-=1
                    if sub_page<0:
                        sub_page=2
                        page-=1
                        article_data = get_list(bbs=bbs,page=page)
            if cmd.strip()=="":
                sub_page+=1
                if sub_page==3:
                    page+=1
                    sub_page=0
                    article_data = get_list(bbs=bbs,page=page,keyword=keyword)
            if cmd.strip()=="\q":
                print("")
                print("안녕히 가십시오. ")
                print("")
                with open(os.path.join(path,'read_log.pkl'),'wb') as fout:
                    pickle.dump(read_log, fout)
                sys.exit()
            if cmd.strip()=="c":
                clear_screen()


def main():
    welcome()
    cmd_line()


if __name__=="__main__":
    main()
