#!/usr/bin/env python

import asyncio
from pyppeteer import launch

from bs4 import BeautifulSoup
from urllib.request import urlopen
import config

# 
from requests_html import HTMLSession
session = HTMLSession()
r = session.get(config.indie_hack_list_url)
r.html.render()
print(r.html.html)
bsObj =  BeautifulSoup(r.html.html)

# for link in  bsObj.find_all("a", {"class": "D9uPgd"}):
# 	if 'href' in link.attrs:
# 		print(link.attrs['href'])
