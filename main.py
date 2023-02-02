#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

import asyncio
import aiohttp
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

# print(title_map)
# print(url_info_map)

async def download_one(url): async with aiohttp.ClientSession() as session: async with session.get(url) as resp: print('Read {} from {}'.format(resp.content_length, url))async def download_all(sites): tasks = [asyncio.create_task(download_one(site)) for site in sites] await asyncio.gather(*tasks)

for index in title_map:
	print(index,title_map[index],url_info_map[index])
