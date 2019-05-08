#!/usr/bin/env python3
# -*- coding: utf8 -*-

import getpass
import os
from api import PixivLoginer
from crawler import mylove
import os.path


if __name__ == '__main__':
    userid = input("请输入用户名：")
    password = getpass.getpass(prompt="请输入密码：")
    saveDir = input("请输入插图保存文件夹路径：")
    path = saveDir

    if not os.path.exists(saveDir):
        os.mkdir(saveDir)

    

    opener = PixivLoginer.login(userid, password)
    
    #pixiv_url_login_test = 'https://i.pximg.net/img-original/img/2018/07/20/08/13/34/69771313_p0.jpg'
     # 下载Pixiv大图测试是否登录成功
    
    
    
    query_tt = mylove.download_first(opener, saveDir)

    p = 456

    while 1==1:
        p += 1
        mylove.download_more(opener, p, saveDir)
