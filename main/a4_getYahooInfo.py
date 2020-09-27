# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 11:06:21 2020

@author: jh
"""
import time

import a0_functions as ct
from lxml import etree
import _thread


def get_info_from_yahoo(str_share_code):
    yahoo_url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=" + str_share_code + ".T"
    yahoo_html = ct.download_html(yahoo_url)
    dom = etree.HTML(yahoo_html)

    # 股票代码
    share_code = dom.xpath('//*[@class="stocksInfo clearFix"]/dt/text()')
    # 股票名
    share_name = dom.xpath('//*[@class="symbol"]/h1/text()')
    # 业种
    industry = dom.xpath('//*[@class="category yjSb"]/a/text()')
    # 最新値
    current_price = dom.xpath('//*[@class="stoksPrice"]/text()')
    # 时间
    current_price_time = dom.xpath('//*[@class="yjSb real"]/span/text()')
    # 前日終値
    yestoday_price = dom.xpath('//*[@class="innerDate"]/div[1]/dl/dd/strong/text()')
    # 始値
    start_price = dom.xpath('//*[@class="innerDate"]/div[2]/dl/dd/strong/text()')
    # 高値
    high_price = dom.xpath('//*[@class="innerDate"]/div[3]/dl/dd/strong/text()')
    # 安値
    low_price = dom.xpath('//*[@class="innerDate"]/div[4]/dl/dd/strong/text()')
    # 出来高
    total_trade_share = dom.xpath('//*[@class="innerDate"]/div[5]/dl/dd/strong/text()')
    # 売買代金
    total_trade_money = dom.xpath('//*[@class="innerDate"]/div[6]/dl/dd/strong/text()')
    # 値幅制限
    limit_price = dom.xpath('//*[@class="innerDate"]/div[7]/dl/dd/strong/text()')
    # 時価総額
    company_total_market_price = dom.xpath('//*[@id="rfindex"]/div[2]/div[1]/dl/dd/strong/text()')
    # 発行済株式数
    company_total_share = dom.xpath('//*[@id="rfindex"]/div[2]/div[2]/dl/dd/strong/text()')
    # 配当利回り（会社予想）
    return_rate = dom.xpath('//*[@id="rfindex"]/div[2]/div[3]/dl/dd/strong/text()')
    # 1株配当（会社予想）
    return_per_share = dom.xpath('//*[@id="rfindex"]/div[2]/div[4]/dl/dd/strong/a/text()')
    # 配当月（会社予想
    return_yymm = dom.xpath('//*[@id="rfindex"]/div[2]/div[4]/dl/dd/span/text()')
    # PER（会社予想）
    per = dom.xpath('//*[@id="rfindex"]/div[2]/div[5]/dl/dd/strong/text()')
    # PBR（実績）
    pbr = dom.xpath('//*[@id="rfindex"]/div[2]/div[6]/dl/dd/strong/text()')
    # EPS（会社予想）
    eps1 = dom.xpath('//*[@id="rfindex"]/div[2]/div[7]/dl/dd/strong/a/text()')
    # BPS（実績）
    eps2 = dom.xpath('//*[@id="rfindex"]/div[2]/div[8]/dl/dd/strong/a/text()')
    # 年初来高値
    high_price_thisyear = dom.xpath('//*[@id="rfindex"]/div[2]/div[11]/dl/dd/strong/text()')
    # 年初来高値日
    high_price_thisyear_date = dom.xpath('//*[@id="rfindex"]/div[2]/div[11]/dl/dd/span/text()')
    # 年初来安値
    low_price_thisyear = dom.xpath('//*[@id="rfindex"]/div[2]/div[12]/dl/dd/strong/text()')
    # 年初来安値日
    low_price_thisyear_date = dom.xpath('//*[@id="rfindex"]/div[2]/div[12]/dl/dd/span/text()')
    # 信用買残
    credit_buy = dom.xpath('//*[@id="margin"]/div/div[1]/div[1]/dl/dd/strong/text()')
    # 信用売残
    credit_sale = dom.xpath('//*[@id="margin"]/div/div[2]/div[1]/dl/dd/strong/text()')

    yahoo_url = "https://stocks.finance.yahoo.co.jp/stocks/profile/?code=" + str_share_code + ".T"
    yahoo_html = ct.download_html(yahoo_url)
    dom = etree.HTML(yahoo_html)

    # 概要
    company_summary = dom.xpath('//*[@name="description"]/@content')
    # 英文社名
    english_name = dom.xpath('//*[contains(text(), "英文社名")]/following-sibling::td[1]/text()')
    # 設立年月日
    company_create_date = dom.xpath('//*[contains(text(), "設立年月日")]/following-sibling::td[1]/text()')
    # 市場名
    company_market_name = dom.xpath('//*[contains(text(), "市場名")]/following-sibling::td[1]/text()')
    # 上場年月日
    company_share_open_date = dom.xpath('//*[contains(text(), "上場年月日")]/following-sibling::td[1]/text()')
    # 決算
    kesan = dom.xpath('//*[contains(text(), "決算")]/following-sibling::td[1]/text()')
    # 本社所在地
    company_address = dom.xpath('//*[contains(text(), "本社所在地")]/following-sibling::td[1]/text()[1]')
    if not len(company_address) == 0:
        print(company_address[0])
        company_address[0] = company_address[0][0:len(company_address[0])-1]
        # company_address[0].replace("[", "")
        print(company_address[0])

    if len(share_name) == 0:
        share_name.append("Error")
    ct.set_defualt_value_to_list(share_name)
    ct.set_defualt_value_to_list(english_name)
    ct.set_defualt_value_to_list(company_market_name)
    ct.set_defualt_value_to_list(industry)
    ct.set_defualt_value_to_list(company_create_date)
    ct.set_defualt_value_to_list(company_share_open_date)
    ct.set_defualt_value_to_list(kesan)
    ct.set_defualt_value_to_list(company_address)
    ct.set_defualt_value_to_list(company_summary)
    ct.set_defualt_value_to_list(company_total_share)
    ct.set_defualt_value_to_list(company_total_market_price)
    ct.set_defualt_value_to_list(return_rate)
    ct.set_defualt_value_to_list(return_per_share)
    ct.set_defualt_value_to_list(return_yymm)
    ct.set_defualt_value_to_list(limit_price)
    ct.set_defualt_value_to_list(per)
    ct.set_defualt_value_to_list(pbr)
    ct.set_defualt_value_to_list(eps1)
    ct.set_defualt_value_to_list(eps2)
    ct.set_defualt_value_to_list(high_price_thisyear)
    ct.set_defualt_value_to_list(high_price_thisyear_date)
    ct.set_defualt_value_to_list(low_price_thisyear)
    ct.set_defualt_value_to_list(low_price_thisyear_date)
    ct.set_defualt_value_to_list(credit_buy)
    ct.set_defualt_value_to_list(credit_sale)
    ct.set_defualt_value_to_list(current_price)
    ct.set_defualt_value_to_list(current_price_time)
    ct.set_defualt_value_to_list(yestoday_price)
    ct.set_defualt_value_to_list(start_price)
    ct.set_defualt_value_to_list(high_price)
    ct.set_defualt_value_to_list(low_price)
    ct.set_defualt_value_to_list(total_trade_share)
    ct.set_defualt_value_to_list(total_trade_money)

    list1 = share_code + \
            share_name + \
            english_name + \
            company_market_name + \
            industry + \
            company_create_date + \
            company_share_open_date + \
            kesan + \
            company_address + \
            company_summary + \
            company_total_share + \
            company_total_market_price + \
            return_rate + \
            return_per_share + \
            return_yymm + \
            limit_price + \
            per + \
            pbr + \
            eps1 + \
            eps2 + \
            high_price_thisyear + \
            high_price_thisyear_date + \
            low_price_thisyear + \
            low_price_thisyear_date + \
            credit_buy + \
            credit_sale + \
            current_price + \
            current_price_time + \
            yestoday_price + \
            start_price + \
            high_price + \
            low_price + \
            total_trade_share + \
            total_trade_money

    # print(";".join(list))
    return list1


listT = ["股票代码",
         "股票名",
         "英文社名",
         "市場名",
         "业种",
         "設立年月日",
         "上場年月日",
         "決算",
         "本社所在地",
         "概要",
         "発行済株式数",
         "時価総額",
         "配当利回り（会社予想）",
         "1株配当（会社予想） ",
         "配当月（会社予想",
         "値幅制限",
         "PER（会社予想） ",
         "PBR（実績） ",
         "EPS（会社予想） ",
         "BPS（実績） ",
         "年初来高値",
         "年初来高値日",
         "年初来安値",
         "年初来安値日",
         "信用買残",
         "信用売残",
         "最新値",
         "时间",
         "前日終値",
         "始値",
         "高値",
         "安値",
         "出来高",
         "売買代金"]


# print(";".join(listT))

def get_info(start, step):
    company_list = ct.get_share_code_list_from_daily_price_db()
    print("一共有多少家公司:",len(company_list))
    while start < len(company_list):
        try:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "No.=", start, ",Share code=", company_list[start])
            # print("i=",start,",",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,",Start Get Info , Share = " +
            # "".join(i))
            list1 = get_info_from_yahoo("".join(company_list[start]))
            if not str(list1[0]) == "Error":
                ct.insert_into_basic_infodb(list1)
            start = start + step
            # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,"i=",start,",Fnished insert into DB, Share = "
            # + "".join(i))
        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "发生了异常")
            start = start + step


# #CompanyList = ct.getCompanyListFromDB()
# #创建两个线程
# try:
#     _thread.start_new_thread(get_info, (0, 10))
#     _thread.start_new_thread(get_info, (1, 10))
#     _thread.start_new_thread(get_info, (2, 10))
#     _thread.start_new_thread(get_info, (3, 10))
#     _thread.start_new_thread(get_info, (4, 10))
#     _thread.start_new_thread(get_info, (5, 10))
#     _thread.start_new_thread(get_info, (6, 10))
#     _thread.start_new_thread(get_info, (7, 10))
#     _thread.start_new_thread(get_info, (8, 10))
#     _thread.start_new_thread(get_info, (9, 10))
#
# except:
#     print("Error: unable to start thread")
#
# while 1:
#     pass
get_info(0, 1)
