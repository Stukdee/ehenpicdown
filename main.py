import requests
from requests.cookies import RequestsCookieJar
import re
from bs4 import BeautifulSoup
from os import makedirs
import multiprocessing
import threading
web_url = 'None'
cookies = 'None'
headers = 'None'
session = requests.Session()
if not cookies == 'None':
	cookie_jar = RequestsCookieJar()
	for k, v in cookies.items():
		cookie_jar.set(k, v)
	session.cookies = cookie_jar
if not headers == 'None':
	session.headers = headers
html = session.get(web_url)
html_text = html.text
title_find = re.search(r'<title>(.*?)</title>',html_text,re.S)
title = title_find.group(1)
path_title = re.sub(r'/',' ',title)
page_find_all = re.findall(r'<td onclick="document.location=this.firstChild.href">.*?<a.*?>(.*?)</a>.*?</td>',html_text,re.S)
all_page = int(page_find_all[len(page_find_all) - 2]) if len(page_find_all) > 1 else 1
def download_image(url : str,number : int,page : int,path : str) -> None:
	image_info = requests.get(url)
	image_type_search = re.search(r'\.([^.]+)$',url)
	image_type = ''
	if image_type_search:
		image_type = image_type_search.group(1)
	full_name = f'{str(page)}-{str(number)}.{image_type}'
	with open(f'./{path}/{full_name}','wb') as f:
		f.write(image_info.content)
def page_download(i : int) -> None:
	print(f'正在浏览第{i + 1}页。')
	page_text = ''
	if i == 0:
		page_text = ''
	else:
		page_text = f'?p={i}'
	page_url = web_url + page_text
	html = session.get(page_url)
	html_text = html.text
	soup = BeautifulSoup(html_text,'lxml')
	urls_div = soup.find('div',id = 'gdt', class_ = 'gt200')
	if urls_div:
		urls_content = str(urls_div)
	urls = re.findall(r'<a href="(.*?)">',urls_content,re.S)
	count : int = 0
	for url in urls:
		count += 1
		print(f'第{i + 1}页第{count}个图片开始下载。')
		html = session.get(url)
		html_text = html.text
		image_url = re.search(r'<img id="img" src="(.*?)".*?>',html_text,re.S)
		download_image(image_url.group(1),count,i + 1,path_title)
	print(f'第{i + 1}页下载完成。')
if __name__ == '__main__':
	print(title)
	makedirs(path_title,exist_ok = True)
	pool = multiprocessing.Pool()
	pages = range(all_page)
	pool.map(page_download,pages)
	pool.close()
	pool.join()
