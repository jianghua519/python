# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:45:17 2020

@author: jh
"""

import datetime
import os
import platform
import zipfile

print(datetime.date.today().strftime("%Y-%m-%d"), ",Start Unzip files..")

if str(platform.platform())[0:3] == "Win":
    strFromPath = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/ZipFiles/"
    strToPath = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/UnzipedFiles/"

else:
    strFromPath = "/volume1/Downloads/ShareAnalyze/Data/ZipFiles/"
    strToPath = "/volume1/Downloads/ShareAnalyze/Data/UnzipedFiles/"

g = os.walk(strFromPath)
for path, dir_list, file_list in g:
    for file_name in file_list:
        if file_name[-4:] == ".zip":
            # print(os.path.join(path, file_name))
            strCSVFile_name = file_name.replace(".zip", ".csv")
            # print(os.path.join(strToPath, strCSVFile_name))
            if not os.path.isfile(strToPath + strCSVFile_name):
                zFile = zipfile.ZipFile(strFromPath + file_name, "r")
                for fileM in zFile.namelist():
                    zFile.extract(fileM, strToPath)
                    print("Unziped:", file_name, "->", fileM)
                    zFile.close()

print(datetime.date.today().strftime("%Y-%m-%d"), ",Finished Unzip files..")
