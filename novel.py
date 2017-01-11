# -*- coding=utf-8 -*-

import requests
import logging

from lxml import html

if __name__ == "__main__":
    #logfile = "/home/emqai/icloud-sync-logs.log"
    logging.basicConfig(level=logging.DEBUG, format = "[%(asctime)s %(filename)s[%(lineno)d]:%(module)s:%(funcName)s %(levelname)s] %(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

    page = requests.get('http://www.baishulou.net/read/0/939/')
    logging.info(page.encoding)
    page.encoding = 'gbk'
    content = page.text#.encode(page.encoding).decode('utf-8')
    logging.info(content)

    tree = html.fromstring(content)
    chapters = tree.xpath("//*[@id='defaulthtml4']/table//td/a/text()")
    print chapters