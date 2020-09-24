import json
import decimal
import time
import numpy

import a0_functions


def str2dec(instr):
    """输入分号分隔的字符串，返回数值List"""
    wk_list1 = instr.split(";")
    wk_list2 = [decimal.Decimal(x) for x in wk_list1]
    return wk_list2


def unpack(in_list):
    out_list = []
    out_dict = {}
    for i in in_list:
        share_code = i[0]
        # print(share_code)
        text = json.loads(i[1])[0]
        new_items = {}
        for key, value in text.items():
            new_items[key] = str2dec(text[key])
        out_list.append([share_code, new_items])
    return out_list


def unpack2dict(in_list):
    out_list = []
    out_dict = {}
    for i in in_list:
        share_code = i[0]
        # print(share_code)
        text = json.loads(i[1])[0]
        new_items = {}
        for key, value in text.items():
            new_items[key] = str2dec(text[key])
        # out_list.append([share_code, new_items])
        out_dict[share_code] = new_items
    return out_dict
    # return out_list


def analyze_gap_rate():
    cl = a0_functions.RunSQL()

    print("start ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    cl.sql = "SELECT  share_code, data_json FROM Cacl_Values_TBL where data_type = 'json'"
    cl.exec_select_sql()
    print("sql   ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    wk_dict = unpack2dict(cl.out_list)
    # x = 0
    # for j in wk_values_list:
    #     for s in j[1].keys():
    #         x = x + 1

    #     {'close_price':list,
    #      'finishi_price_change_rate':list,
    #      'price_change':list,
    #      'inday_price_change_rate':list,
    #      'total_trade_money':list
    #      'str_growth_rete':list
    #      }
    # ]

    #
    # 计算活跃指数
    # 计算出每日的振幅     再求平方     然后求平均     再开方乘10     即可
    # 结果在0 - 100     之间     越高越活跃

    wk_huoyue_list = []
    for share_code in wk_dict.keys():
        i = 1
        x = 0
        for values in wk_dict[share_code]['inday_price_change_rate']:
            x = x + values * values
        avg = x / len(wk_dict[share_code]['inday_price_change_rate'])
        result = numpy.sqrt(avg) * 10
        print(share_code, '的活跃指数=', result)

    # for i in cl.out_list:
    #     x = i[1].split(";")
    #     k = 0
    #     for j in x:
    #         if Decimal(j) > 8:
    #             k = k + 1
    #     if k > 90:
    #         print(i[0], ",", i[2], "高低差超过8%的天数=", k)


def share_select():
    cl = a0_functions.RunSQL()

    print("start ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    cl.sql = "SELECT  share_code, data_json FROM Cacl_Values_TBL where data_type = 'json'"
    cl.exec_select_sql()
    print("sql   ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    wk_dict = unpack2dict(cl.out_list)
    select_set = {"活跃指数": [], "涨跌幅>10": [], "近期低价": []}

    for share_code in wk_dict.keys():
        # 涨停前后3天
        i = 1
        x = 0

        # 活跃指数
        i = 1
        x = 0
        for values in wk_dict[share_code]['inday_price_change_rate']:
            x = x + values * values
        avg = x / len(wk_dict[share_code]['inday_price_change_rate'])
        result = numpy.sqrt(avg) * 10
        if result > 40:
            select_set["活跃指数"].append(share_code)

        # 涨跌幅大于2
        abs_list = [abs(i) for i in wk_dict[share_code]['price_change'][-10:]]
        # print(abs_list)
        if numpy.mean(abs_list) > 10:
            select_set["涨跌幅>10"].append(share_code)

        # 近期低价
        max1 = max(wk_dict[share_code]['close_price'][-50:])
        min1 = min(wk_dict[share_code]['close_price'][-50:])
        # min2 = min(wk_dict[share_code]['close_price'][-600:])
        avg1 = numpy.mean(wk_dict[share_code]['close_price'][-3:])
        if min1 + (decimal.Decimal(0.1) * (max1 - min1)) > avg1:
            select_set["近期低价"].append(share_code)
            # if numpy.mean(wk_dict[share_code]['price_change'][-5:]) < \
            #         decimal.Decimal(0.6) * numpy.mean(wk_dict[share_code]['price_change'][-30:]):
            select_set["近期低价"].append(share_code)

    print(len(select_set["活跃指数"]))
    print(len(select_set["涨跌幅>10"]))
    print(len(select_set["近期低价"]))
    print(" ")
    for i in select_set["活跃指数"]:
        if i in select_set["涨跌幅>10"] and i in select_set["近期低价"]:
            print(i)



# analyze_gap_rate()
share_select()
