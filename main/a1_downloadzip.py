# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 13:21:59 2020

@author: jh
"""
import os
import platform
import datetime


# 两个参数 URL，要保存的文件路径
import urllib
from urllib.request import urlopen


def func_download_data(iurl, outfilename):
    # 如果已经取得过，就不再取得

    if os.path.isfile(outfilename):
        # print ('Exist,Output File:', outfilename)
        return

    if os.path.isfile(outfilename + ".NG.txt"):
        # print ('Exist,Output File:', outfilename + ".NG.txt")
        return

    # 从WEB上取得数据。
    try:
        response = urlopen(iurl)
    # 如果出错，就放一个NG.txt文件
    except urllib.error.HTTPError:
        print('NG,Input URL::', iurl)
        open(outfilename + ".NG.txt", 'wb').close()
        return

    # 把取得的数据，写入文件
    req = response.read()
    with open(outfilename, 'wb') as f:
        f.write(req)
        f.close()
    print('OK,Input URL::', iurl, ',Output File:', outfilename)
    return


print(datetime.date.today().strftime("%Y-%m-%d"), ",Start  DownloadData.")

strYear1 = '20'
strYear2 = '20'
strMonth = '09'
strDay = '01'

if str(platform.platform())[0:3] == "Win":
    string_path_prefix = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/ZipFiles/T"
else:
    string_path_prefix = "/volume1/Downloads/ShareAnalyze/Data/ZipFiles/T"

dateWkDate = datetime.datetime.strptime('2020-01-01', "%Y-%m-%d")
strWKDate = dateWkDate.strftime("%Y-%m-%d")

while strWKDate <= datetime.date.today().strftime("%Y-%m-%d"):
    strYear2 = strWKDate[2:4]
    strMonth = strWKDate[5:7]
    strDay = strWKDate[8:10]

    url1 = 'http://mujinzou.com/d_data/' + strYear1 + strYear2 + 'd/' + strYear2 + \
           '_' + strMonth + 'd/T' + strYear2 + strMonth + strDay + '.zip'

    out_file_name = string_path_prefix + strYear2 + strMonth + strDay + ".zip"

    func_download_data(url1, out_file_name)
    dateWkDate = dateWkDate + datetime.timedelta(1)
    strWKDate = dateWkDate.strftime("%Y-%m-%d")

print(datetime.date.today().strftime("%Y-%m-%d"), ",Finished DownloadData.")
