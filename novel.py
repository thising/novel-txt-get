# -*- coding=utf-8 -*-

import requests
import os
import logging
import datetime

from lxml import html

if __name__ == "__main__":
    #logfile = "/home/emqai/icloud-sync-logs.log"
    #logging.basicConfig(level=logging.DEBUG, format = "[%(asctime)s %(filename)s[%(lineno)d]:%(module)s:%(funcName)s %(levelname)s] %(message)s", datefmt = "%Y-%m-%d %H:%M:%S")
    logging.basicConfig(level=logging.DEBUG)

    # settings 古人医
    #novel_name = '古人医'
    #work_dir = '/tmp/'
    #menu_url = 'http://www.baishulou.net/read/0/939/'
    #menu_link_path = "//*[@id='defaulthtml4']/table//td/a"
    #chapter_text_path = "//*[@id='content']/text()"
    #encoding = 'gbk'
    #timeout = 30

    # settings 偷香
    # novel_name = '偷香'
    # work_dir = '/tmp/'
    # menu_url = 'http://www.dajiadu.net/files/article/html/25/25375/'
    # menu_link_path = "//*[@id='booktext']//li/a"
    # chapter_text_path = "//*[@id='content1']/text()"
    # encoding = 'gbk'
    # timeout = 30

    # settings 都市极品风水师
    novel_name = '都市极品风水师'
    work_dir = '/tmp/'
    menu_url = 'http://www.piaotian.com/html/5/5350/'
    menu_link_path = "/html/body/div[4]/div[1]/div[2]/ul/li/a"
    chapter_text_path = "/html/body//text()"
    encoding = 'gbk'
    timeout = 30

    # start
    menu_page = requests.get(menu_url, timeout = timeout)
    menu_page.encoding = encoding

    menu_tree = html.fromstring(menu_page.text)
    menu_links = menu_tree.xpath(menu_link_path)

    novel_file = os.path.join(work_dir, (novel_name + '.txt'))
    with open(novel_file, 'w+') as out_file:
        out_file.write("%s\n\n" % novel_name)
        out_file.write("generated by <novel-txt-get> on <%s>\n\n\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for link in menu_links:
            try:
                chapter_url = menu_url + link.get('href')
                chapter_title = link.text
                out_file.write('===============\n%s\n===============\n*source url:%s\n\n' % (chapter_title.encode('utf-8'), chapter_url))
                logging.info('Start to get <%s> from <%s> ...', chapter_title, chapter_url)
                chapter_page = requests.get(chapter_url, timeout = timeout)
                chapter_page.encoding = encoding
                chapter_tree = html.fromstring(chapter_page.text)
                chapter_text_nodes = chapter_tree.xpath(chapter_text_path)
                text = '\n'.join(i for i in chapter_text_nodes)
                out_file.write("%s\n\n" % text.encode('utf-8'))
                logging.info('Success.')
            except Exception, e:
                logging.info('Failed. %r', e)
                out_file.write("FAILED.\n\n")
                continue
        out_file.close()