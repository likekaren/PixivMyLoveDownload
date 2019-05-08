#!/usr/bin/env python3
# -*- coding: utf8 -*-

import getpass
import json
import os.path
import time
from bs4 import BeautifulSoup
import utils
from api import PixivLoginer
from crawler import Pixivlove

pixiv_url_love = 'https://www.pixiv.net/bookmark.php?rest=show&p=1'

query_format = 'json'

def analysis_html(html):
    items = []
    rootSoup = BeautifulSoup(html, 'lxml')
    
    selector = rootSoup.select('#wrapper > div.layout-a > div.layout-column-2 > div._unit > form > div.display_editable_works > ul > li')
    
    for child in selector:

        try:
            thumbnailUrl = child.select('a.work > div > img')[0]['data-src']
            originalUrl1 = thumbnailUrl.replace('c/150x150/img-master', 'img-original')
            originalUrl1 = originalUrl1.replace('p0_master1200', 'p0')
            originalUrl2 = thumbnailUrl.replace('c/150x150/img-master', 'c/1200x1200/img-master')

            items.append(Pixivlove(originalUrl1, originalUrl2))
        except Exception as e:
            pass
    
    return items
    

def analysis_json(js):

    items = []

    contents = json.loads(js)['contents']

    for child in contents:
        thumbnailUrl = child.select('a.work > div > img')[0]['data-src']

        originalUrl1 = thumbnailUrl.replace('c/150x150/img-master', 'img-original')
        originalUrl1 = originalUrl1.replace('p0_master1200', 'p0')
        originalUrl2 = thumbnailUrl.replace('c/150x150/img-master', 'c/1200x1200/img-master')

        items.append(Pixivlove(originalUrl1, originalUrl2))

    return items


def get_tt(html):
    rootSoup = BeautifulSoup(html, 'lxml')
    tt = rootSoup.select('#wrapper > footer > div > ul > li')[0].select('form > input')[1]['value']
    return tt


def download_illustration(op, items, picDir):

    print("正在下载中……")

    for item in items:
        try:
            with op.open(item.originalUrl1) as op_img1:
                if op_img1.status == 200:
                    with open(os.path.join(picDir, item.originalUrl1.split('/')[-1]), 'wb') as o:
                        o.write(op_img1.read())
                        print('图片已成功下载 -> 社保了')
        except Exception as e:
            try:
                with op.open(item.originalUrl2) as op_img2:
                    if op_img2.status == 200:
                        with open(os.path.join(picDir, item.originalUrl2.split('/')[-1]), 'wb') as o:
                            o.write(op_img2.read())
                            print('图片已成功下载 -> 社保了')
            except Exception as e:
                pass

        # 等待1秒，爬得太快容易被发现(￣▽￣)"
        time.sleep(1)

    print("当前页下载完成，我的身体已经菠萝菠萝大！")


def download_first(op, picDir):
    visit = pixiv_url_love
    
    tt = None
    items = None
    try:
        with op.open(visit) as f:
            if f.status == 200:
                html = utils.ungzip(f.read()).decode()
            
                tt = get_tt(html)
                items = analysis_html(html)
    except Exception as e:
        pass

    if items:
        download_illustration(op, items, picDir)
    
    return tt


def download_more(op, p, picDir):
    visit = 'https://www.pixiv.net/bookmark.php?rest=show&p=' + str(p)
    print("开始下载第%s页"%p)
    
    items = None

    with op.open(visit) as f:
        if f.status == 200:
            html = utils.ungzip(f.read()).decode()
            
            tt = get_tt(html)
            items = analysis_html(html)

    if items:
        download_illustration(op, items, picDir)


if __name__ == '__main__':
    userid = input("请输入用户名：")
    password = getpass.getpass(prompt="请输入密码：")
    saveDir = input("请输入插图保存文件夹路径：")

    if not os.path.exists(saveDir):
        os.mkdir(saveDir)

    opener = PixivLoginer.login(userid, password)
    

    # 下载第一页插图，并获取重要参数tt
    query_tt = download_first(opener, saveDir)

    p = 1

    while 1==1:
        p += 1
        download_more(opener, p, saveDir)
        
