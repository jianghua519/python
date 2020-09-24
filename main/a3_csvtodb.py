# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 23:45:43 2020

@author: jh
"""

import csv
import os
import sys
import time
import mariadb

strPath = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/UnzipedFiles/"

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ", Start process Csv Files, Path=", strPath)

g = os.walk(strPath)
i = 1
for path, dir_list, file_list in g:
    for file_name in file_list:
        if file_name[-4:] == ".csv" and not os.path.isfile(strPath + file_name + ".ok"):
            if not os.path.isfile(strPath + file_name + ".ok"):

                # Connect to MariaDB Platform
                try:
                    conn = mariadb.connect(
                        user="jianghua519",
                        password="#JH123456xw",
                        host="192.168.31.240",
                        port=3307,
                        database="jianghua519"
                    )
                except mariadb.Error as e:
                    print(f"Error connecting to MariaDB Platform: {e}")
                    sys.exit(1)

                # Get Cursor
                cur = conn.cursor()
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ", Instert into DB :", strPath + file_name,
                      ",current line=", i)
                with open(strPath + file_name, newline='', encoding='cp932') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    # print(spamreader)
                    for row in spamreader:
                        try:
                            cur.execute(
                                "INSERT INTO `DailyShareInfo`(`trade_date`, `share_code`, `industry_code`, "
                                "`share_name`, `start_price`, `high_price`, `low_price`, `finishi_price`, "
                                "`trade_total`, `market`) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s)",
                                row)
                        except mariadb.Error as e:
                            print("     Error record=", row)
                        i = i + 1
                conn.commit()
                conn.close()
                open(strPath + file_name + ".ok", 'wb').close()

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ", Finish process Csv Files")
