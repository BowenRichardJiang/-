import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
requests.adapters.DEFAULT_RETRIES = 15
s = requests.session()
s.keep_alive = False
tjbg_url = 'http://www.tjcn.org/tjgbsy/nd/35757.html' #修改年份网址
tjbg_html = requests.get(tjbg_url,  headers=headers)
tjbg_html.encoding = 'gb18030'
Soup=BeautifulSoup(tjbg_html.text, 'lxml')
all_a=Soup.find('div',class_='sy').find_all('a')

for k in all_a:
    href = 'http://www.tjcn.org/' + k['href']
    name = k.get_text()
    if "市" in name:
        html_url = requests.get(href, headers=headers)
        html_url.encoding = 'gb18030'
        html_Soup = BeautifulSoup(html_url.text, 'lxml')
        text = html_Soup.find('td', id='text').text
        index = text.find("住户贷款")
        if index != -1:
            print(text[index:index + 15])
            print(name + "结束")
            continue
        length = len(href)
        for i in range(2, 20):
            new_href = href.replace(".html", "_"+str(i)+".html")
            html_url = requests.get(new_href, headers=headers)
            if html_url.status_code == 404:
                break
            html_url.encoding = 'gb18030'
            html_Soup = BeautifulSoup(html_url.text, 'lxml')
            text = html_Soup.find('td', id='text').text
            index = text.find("住户贷款")
            if index != -1:
                print(text[index:index+15])
                break
        time.sleep(10)
    print(name + "结束")