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
    out_dict = {}
    for i in in_list:
        share_code = i[0]
        # print(share_code)
        text = json.loads(i[1])[0]
        new_items = {}
        for key, value in text.items():
            if not key == 'trade_date':
                new_items[key] = str2dec(text[key])
        # out_list.append([share_code, new_items])
        out_dict[share_code] = new_items
    return out_dict
    # return out_list


def share_select():
    out_list = []
    cl = a0_functions.RunSQL()
    ds = a0_functions.DiaplayShareInfo()

    print("start ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    cl.sql = "SELECT  share_code, data_json FROM Cacl_Values_TBL where data_type = 'json'"
    cl.exec_select_sql()
    print("sql   ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    wk_dict = unpack2dict(cl.out_list)
    select_set = {"活跃指数": [], "涨跌幅>10": [], "近期低价": [], "中等价位股": [], "近几天成交量放大": []}

    for share_code in wk_dict.keys():

        # 中等价位股
        x = 0
        if numpy.mean(wk_dict[share_code]['close_price'][-5:]) < 5000:
            select_set["中等价位股"].append(share_code)

        # 活跃指数
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

        # 近几天成交量放大
        avg1 = numpy.mean(wk_dict[share_code]['close_price'][-1:])
        avg3 = numpy.mean(wk_dict[share_code]['close_price'][-4:-2])
        if avg1 > avg3 * decimal.Decimal(1.2):
            select_set["近几天成交量放大"].append(share_code)

        # 近期低价
        max1 = max(wk_dict[share_code]['close_price'][-50:])
        min1 = min(wk_dict[share_code]['close_price'][-50:])
        avg1 = numpy.mean(wk_dict[share_code]['close_price'][-3:])
        if min1 + (decimal.Decimal(0.1) * (max1 - min1)) > avg1:
            select_set["近期低价"].append(share_code)

    print("中等价位股数量=", len(select_set["中等价位股"]))
    print("活跃指数股数量=", len(select_set["活跃指数"]))
    print("涨跌幅较大股数量=", len(select_set["涨跌幅>10"]))
    print("近期低价股数量=", len(select_set["近期低价"]))
    print(" ")
    for i in select_set["活跃指数"]:
        if i in select_set["涨跌幅>10"] and \
                i in select_set["中等价位股"] and \
                i in select_set["近期低价"]:
            ds.print_share_info(share_code=i)
            out_list.append(i)
        # if i in select_set["近几天成交量放大"]:
        #     print("近几天成交量放大", i)
        #     # ds.print_share_info(share_code=i)
    return out_list


# analyze_gap_rate()
# callable()

rs = a0_functions.RunSQL()
lable = "autoSelected"
content = []
for i in share_select():
    rs.sql = "select share_code, share_name ,industry, company_marketname from BasicCompanyInfo " \
             "where industry != ' ' and share_code ='{}'".format(i)
    rs.exec_select_sql()
    if len(rs.out_list) > 0:
        content.append(",".join(rs.out_list[0]))

rs.sql = "delete from Cache_Table where cache_lable like '{}'".format(lable)
rs.exec_update_sql()
rs.sql = "INSERT INTO `Cache_Table` (`id`, `cache_lable`, `cache_content`) " \
         "VALUES (NULL, '{}', '{}')".format(lable, ';'.join(content))
rs.exec_update_sql()
