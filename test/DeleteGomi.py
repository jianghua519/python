# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 01:10:51 2020

@author: jh
"""

# 一致する銘柄は見つかりませんでした


# from DownloadData import funcDownloadData

import platform, os

# from bs4 import BeautifulSoup


if str(platform.platform())[0:3] == "Win":
    strPathprifix = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/CompanyInfoFiles/Y"
else:
    strPathprifix = "/volume1/Downloads/ShareAnalyze/Data/CompanyInfoFiles/Y"

i = 1001
while i < 9999:
    outfilename = strPathprifix + str(i) + ".html"
    # url1 = "https://xn--vckya7nx51ik9ay55a3l3a.com/companies/" + str(i)
    url1 = "https://stocks.finance.yahoo.co.jp/stocks/profile/?code=" + str(i) + ".T"
    # url1 = "https://上場企業サーチ.com/companies/" + str(i)
    exampleFile = open(strPathprifix + str(i) + ".html")
    r = exampleFile.read()
    if r.find("一致する銘柄は見つかりませんでした") > 0:
        exampleFile.close()
        os.remove(outfilename)
        open(outfilename + ".NG.txt", 'a').close()
        # print("    Useless file",outfilename)
    else:
        exampleFile.close()
        # print("USEFULL file",outfilename)
    i = i + 1

