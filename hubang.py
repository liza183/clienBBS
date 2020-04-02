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
        
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://www.clien.net',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://www.clien.net/service/login',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        login_req = s.post(login_url, headers=headers, data=user_info)
        
        if login_req.status_code != 200:
            print ('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
        else:
            print ('로그인에 성공 하였습니다.')
            logged_in_user = user_info['userId']
            return s

    print("로그인을 할수 없습니다. ")
    return None

 
def get_list(page_max=0):
        global login_session
        data = []
        for page in range(0, page_max):
            print("Processing page:", page, "...")
            new_url = "https://www.clien.net/service/search/board/park?sk=title&sv=%ED%9B%84%EB%B0%A9&po="+str(page)
            #print(page, new_url)
            if login_session is not None:
                page_data = Soup(login_session.get(new_url, verify=cert_path).text, 'lxml')
            else:
                page_data = Soup(requests.get(new_url, verify=cert_path).text, 'lxml')
            
            list_article = page_data.findAll("div", {"data-role": "list-row"})
            
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
    print("Login successful!")
    print()

    item_list = get_list(page_max=100)

    for item in item_list:

        try:
            article_url = "http://clien.net"+item[2]
            article_data_soup = Soup(login_session.get(article_url,verify=cert_path).text, 'lxml')    
            imgs = article_data_soup.find("div", {"class": "post_content"}).findAll("img")
            idx = 0
            for img in imgs:
                print(idx, img["src"], "downloading ..")
                urllib.request.urlretrieve(img['src'], "downloaded/"+img['src'].split("/")[-1].split("?")[0])
                time.sleep(3)
                idx+=1
        except:
            print("Some error occurred while processing", item)