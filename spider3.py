import requests
from pyquery import PyQuery as pq
import re
import base64
from urllib import parse
import sqlite3
import threading
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.163 Safari/537.36 ',
    'referer': 'https://www.XXXX.xyz/list.php?class=guochan',
    'Connection': 'keep-alive'
}


def exe_js(any_bytes):
    c = base64.b64decode(any_bytes)
    d = parse.quote(c)
    d = parse.unquote(d)
    return d


def exe(table_name, start_page_num, end_page_num):
    conn = sqlite3.connect('spider.db')
    print('链接成功')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS {} (date TEXT,title TEXT,url TEXT)".format(table_name))
    print('建表成功')

    def hhh(page_url):
        try:

            s = requests.Session()
            req = s.get(url=page_url, headers=headers, timeout=5)
            page = req.text
            print('网页抓取成功',end="")

            doc = pq(page)
            html = doc('ul.list')
            html.find('li:first-child').remove()
            html.find('li:last-child').remove()

            html = html.html()

            result = re.findall(
                '<li>(.*?)<a.*?href="(.*?)".*?d\((.*?)\).*?</li>', html, re.S)

            for i in result:
                date = i[0]
                url = 'https://www.XXXX.xyz' + i[1]
                url = re.sub('amp;', '', url)
                js_a = eval('b' + i[2])
                title = exe_js(js_a)
                title = re.sub('<.*?>', '', title)
                c.execute("INSERT INTO {} (date,title,url) VALUES('{}','{}','{}')".format(
                    table_name, date, title, url))

        except:
            print('错误,重试ing',end="")
            hhh(page_url)

    for index in range(start_page_num, end_page_num + 1):
        page_url = 'https://www.XXXX.xyz/list.php?class=guochan&page={}'.format(
            index)
        hhh(page_url)
        conn.commit()
        print('第{}页抓取完毕'.format(index))
        time.sleep(2)

    conn.close()
    print('链接关闭')


if __name__ == '__main__':
    c = threading.Thread(target=exe,args=('first',1,50))
    d = threading.Thread(target=exe,args=('first',51,100))
    e = threading.Thread(target=exe,args=('first',101,150))
    f = threading.Thread(target=exe,args=('first',151,200))
    c.start()
    d.start()
    e.start()
    f.start()