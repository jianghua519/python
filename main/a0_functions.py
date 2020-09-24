# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:32:37 2020

@author: jh

这个程序根据输入的URL从互联网取得数据，存到磁盘文件
"""

import codecs
import csv
import sys
import urllib
from urllib.request import urlopen

import pymysql


class RunSQL:

    def __init__(self):
        self.connect_db()
        # print("DB connected ")

    def __del__(self):
        self.conn.close()
        # print("DB closed ")

    conn = None
    sql = ""
    out_list = []

    def connect_db(self):
        try:
            self.conn = pymysql.connect(user="jianghua519", password="#JH123456xw", host="192.168.31.240", port=3307,
                                        database="jianghua519")
        except pymysql.Error as e:
            print("DB connect error : ", e)
            exit(4)

    def exec_update_sql(self):
        try:
            cur = self.conn.cursor()
            cur.execute(self.sql)
            self.conn.commit()
            cur.close()

        except pymysql.Error as e:
            print('DB update  error : ', e)
            print('Error sql:', self.sql)
            exit(4)

    def exec_select_sql(self):
        try:
            cur = self.conn.cursor()
            cur.execute(self.sql)
            self.out_list = list(cur)
            cur.close()

        except pymysql.Error as e:
            print('DB select error : ', e)
            exit(4)


def insert_into_basic_infodb(list1):
    try:
        connect = pymysql.connect(user="jianghua519", password="#JH123456xw", host="192.168.31.240", port=3307,
                                  database="jianghua519")
        conn = connect
    except pymysql.Error as e:
        print("Error connecting to pymysql Platform:", e)
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM `BasicCompanyInfo` WHERE `BasicCompanyInfo`.`share_code` = '{}'".format(list1[0]))
        cur.execute("INSERT INTO `BasicCompanyInfo` VALUES "
                    + "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,"
                    + "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,"
                    + "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,"
                      "%s, %s, %s, %s)", list1)

    except pymysql.Error as e1:
        print("Error insert data to pymysql ", e1)

    conn.commit()
    conn.close()


def get_share_code_list_from_daily_price_db():
    try:
        conn = pymysql.connect(
            user="jianghua519",
            password="#JH123456xw",
            host="192.168.31.240",
            port=3307,
            database="jianghua519"
        )
    except pymysql.Error as e:
        print("Error connecting to pymysql Platform:", e)
        sys.exit(1)

    company_list3 = []

    # Get Cursor
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT DISTINCT share_code FROM `DailyShareInfo` WHERE `trade_date` = ( SELECT max( trade_date ) from "
            "DailyShareInfo)")
        company_list1 = list(cur)
        # print(len(company_list1))
        # cur.execute("SELECT DISTINCT share_code FROM `BasicCompanyInfo`")
        # company_list2 = list(cur)
        # print(len(company_list2))
        # company_list3 = [x for x in company_list1 if x not in company_list2]
        # print(len(company_list3))
    except pymysql.Error as e1:
        print("Error select data from db: ", e1)

    conn.commit()
    conn.close()
    return company_list1


def db_to_list_and_csv(sql, out_list=None, out_csv_path: str = "No need") -> object:
    """
    根据给定的SQL文，检索DB并输出为CSV文件，或输出为list
    :return: 0: OK , 4: NG
    """
    return_code = 4
    try:
        conn = pymysql.connect(user="jianghua519", password="#JH123456xw", host="192.168.31.240", port=3307,
                               database="jianghua519")

    except pymysql.Error as e:
        print("Error connecting to pymysql Platform: ", e)
        sys.exit(1)

    if out_list is None and out_csv_path == "No need":
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return 0

    # Get Cursor
    cur = conn.cursor()
    try:
        cur.execute(sql)
        out_list.extend(list(cur))
        if not out_csv_path == "No need":
            f = codecs.open(out_csv_path, 'w', 'utf_8_sig')
            writer = csv.writer(f)
            for i in out_list:
                writer.writerow(i)
            f.close()
            # f = open(out_csv_path, 'r')
            # text = f.read()
            # f.close()
            # text = text.replace(',', '')
            # f = open(out_csv_path, 'w')
            # f.write(text)
            # f.close

        return_code = 0

    except pymysql.Error as e:
        print("Error execute sql: ", e)

    conn.commit()
    conn.close()
    return return_code


def download_html(iurl):
    # print("Debug---,input url="+iurl)
    # 从WEB上取得数据。
    try:
        response = urlopen(iurl)
    # 如果出错，返回message
    except urllib.error.HTTPError:
        print("Debug---,Error url=" + iurl)
        out_string = "##Open URL Error##, " + iurl
        return out_string

    # 把取得的数据，写入文件
    req = response.read()
    return req


def set_defualt_value_to_list(list1):
    if len(list1) == 0:
        list1.append(" ")


class DiaplayShareInfo:
    rs = None

    def __init__(self):
        self.rs = RunSQL()
        # print("DB connected ")

    def print_share_info(self, share_code):
        self.rs.sql = "SELECT `share_code`, `share_name`, `Company_MarketName`, `industry` FROM `BasicCompanyInfo` " \
                      "Where share_code = '{}'".format(share_code)
        self.rs.exec_select_sql()
        out_str = ",".join(self.rs.out_list[0])
        self.rs.sql = "SELECT `finishi_price`, `trade_total` FROM `DailyShareInfo` WHERE share_code = '{}' and " \
                      "`trade_date` = (select DISTINCT max(trade_date) from DailyShareInfo) ".format(share_code)
        self.rs.exec_select_sql()
        out_str = out_str + ",收盘价=" + str(self.rs.out_list[0][0]) + ",成交量=" + str(self.rs.out_list[0][1])
        print(out_str)
