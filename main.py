#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import concurrent.futures
import threading
import time


import config

def scrap():
	session = HTMLSession()
	r = session.get(config.indie_hack_list_url)
	r.html.render()
	print(r.html.html)
	bsObj =  BeautifulSoup(r.html.html)
	return bsObj

def get_mp3_info():
	bsObj = scrap()
	for link in  bsObj.find_all("div", {"jsname": "fvi9Ef"}):
		if 'jsdata' in link.attrs:
			print(link.attrs['jsdata'])
	
def get_titles():
	bsObj = scrap()
	for div in  bsObj.find_all("div", {"class": "e3ZUqe"}):
				print(div.getText())

def download_mp3(url,filename):
	doc = requests.get(url)
	with open(filename,'wb') as f:
		f.write(doc.content)

title_map = {}
with open("title.txt", "r") as f:
	for line in f.readlines():
		info = line.split(" – ")
		title_map[info[0]] = info[1]

url_info_map = {}	

with open("url.txt", "r") as f:
	for line in f.readlines():
		info = line.split(";")
		url_info_map[info[1].strip("\n")] = info[0]
	
def download_mp3_with(index):
	url = url_info_map[index]
	filename = "data/" + "ih#" + index +"#" + title_map[index] + ".mp3"
	download_mp3(url,filename)

def download_all(indexs): 
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: 
		executor.map(download_mp3_with, indexs)

all_indexs = title_map.keys() 
download_all(all_indexs)