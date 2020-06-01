import requests
from bs4 import BeautifulSoup
import re
import json
import time

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            code=re.findall(r"s[hz]\d{6}", href)[0]
            if 'sh'.__eq__(code[:2]):
                code='0'+code[2:]
            if 'sz'.__eq__(code[:2]):
                code='1'+code[2:]
            lst.append(code)
        except:
            continue
    print(f'获取链接共{len(lst)}条')


def getStockInfo(lst, stockURL, fpath):
    count = 0

    for stock in lst[-100:]:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'relate_stock clearfix'})
            name = stockInfo.find('script').next_element[30:]
            a = re.compile(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
            clean_str = a.sub('', name)
            print(clean_str)

        except:
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stock_list.html'
    stock_info_url = 'http://quotes.money.163.com/'
    output_file = 'F:\BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

time1 = time.time()
main()
print(time.time()-time1)