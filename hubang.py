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

import requests
import os
import sys
import certifi
import time
import urllib
import os

base_url = "https://www.clien.net"
login_url = 'https://www.clien.net/service/login'
global login_session
global logged_in_user
login_session = None
logged_in_user = None
global url
url = "https://www.clien.net/service/board/park?&od=T31&po="


def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                        relative)

cert_path = resource_path(certifi.where())

def set_csrf(page, param):
    html = page.text
    soup = Soup(html, 'html.parser')
    csrf = soup.find('input', {'name': '_csrf'})
    return {**param, **{'_csrf': csrf['value']}}

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

 
def get_list(page=0, keyword=None):
        global login_session
        data = []
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
                    comment_no = item.findAll("span",{"class":"rSymph05"})[0].text
                except:
                    comment_no = ""                    
                hits = item.findAll("div")[3].span.text
                link = item.find("a",{"class":"list_subject"})['href']
                author = item['data-author-id'].strip()
                timestamp = item.find("div",{"class":"list_time"}).span.span.text
                data.append((title,author,link,hits,timestamp,comment_no))
        return data

if __name__=="__main__":
    login_session = login()
    for item in get_list(keyword=".jpg"):
        article_url = "http://clien.net"+item[2]
        article_data_soup = Soup(login_session.get(article_url,verify=cert_path).text, 'lxml')    
        imgs = article_data_soup.find("div", {"class": "post_content"}).findAll("img")
        idx = 0
        for img in imgs:
            print idx, img["src"], "downloading .."
            urllib.request.urlretrieve(img['src'], "downloaded/"+img['src'].split("/")[-1].split("?")[0])
            time.sleep(3)
            idx+=1
        