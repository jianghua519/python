import datetime
import json
import decimal

import a0_functions


def get_all_date_and_share():
    cl = a0_functions.RunSQL()

    # 一年前的今天的日期
    today_of_lastyear = datetime.datetime.now() - datetime.timedelta(days=366)

    # 检索一年前以来的日期
    cl.sql = "SELECT DISTINCT trade_date FROM `DailyShareInfo` where trade_date > '" \
             + today_of_lastyear.strftime('%Y-%m-%d') + "' ORDER by trade_date"
    cl.exec_select_sql()
    wk_list = [cl.out_list[i][0].strftime("%Y-%m-%d") for i in range(1, len(cl.out_list))]
    wk_str = ";".join(wk_list)

    last_trade_day = cl.out_list[-1][0].strftime("%Y-%m-%d")
    standard_count_of_days = len(cl.out_list)

    # 删除过去的内容
    cl.sql = "DELETE FROM `Cacl_Values_TBL`"
    cl.exec_update_sql()

    # 把日期写入DB
    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('0000', 'date', '" + wk_str + "')"
    cl.exec_update_sql()

    wk_list = [cl.out_list[i][0].strftime("%Y-%m-%d") for i in (0, 1, len(cl.out_list) - 1)]
    wk_list.append(str(standard_count_of_days))
    wk_str = ";".join(wk_list)

    # 把参照用日期写入DB
    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('0000', 'date_ref', '" + wk_str + "')"
    cl.exec_update_sql()

    # 得到股票列表并写入DB
    cl.sql = "SELECT  share_code FROM `DailyShareInfo` where trade_date = '" \
             + last_trade_day + "'"
    cl.exec_select_sql()

    wk_list = [str(i[0]) for i in cl.out_list]
    wk_str = ";".join(wk_list)

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('0000', 'all_share_code', '" + wk_str + "')"
    cl.exec_update_sql()


def calc_values(share_code, value_type, from_date, standard_count_of_days=0):
    cl = a0_functions.RunSQL()

    # 查询1001信息，得到 days
    if standard_count_of_days == 0:
        cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
                 " share_code = '{}' ORDER by trade_date ".format(value_type, from_date, '1001')
        cl.exec_select_sql()

        standard_count_of_days = len(cl.out_list)

    # 查询指定信息
    cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
             " share_code = '{}' ORDER by trade_date ".format(value_type, from_date, share_code)
    cl.exec_select_sql()

    wk_list = [str(i[0]) for i in cl.out_list]

    while len(wk_list) < standard_count_of_days:
        wk_list.insert(0, '0.00')

    del (wk_list[0])
    wk_str = ";".join(wk_list)
    print(share_code, value_type, len(wk_list))

    # 把值写入DB
    cl.sql = "delete from Cacl_Values_TBL where  ( share_code = '{}' and data_type = '{}')".format(share_code,
                                                                                                   value_type,
                                                                                                   wk_str)
    cl.exec_update_sql()

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('{}', '{}', '{}')".format(share_code, value_type, wk_str)
    cl.exec_update_sql()


def cacl_change_rates(share_code, value_type, from_date, standard_count_of_days=0):
    cl = a0_functions.RunSQL()

    # 查询1001信息，得到 days
    if standard_count_of_days == 0:
        cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
                 " share_code = '{}' ORDER by trade_date ".format(value_type, from_date, '1001')
        cl.exec_select_sql()

        standard_count_of_days = len(cl.out_list)

    # 查询指定信息
    cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
             " share_code = '{}' ORDER by trade_date ".format(value_type, from_date, share_code)
    cl.exec_select_sql()

    wk_list = [i[0] for i in cl.out_list]

    while len(wk_list) < standard_count_of_days:
        wk_list.insert(0, 0.00)

    wk_change_rate_list = []
    for i in range(1, len(wk_list)):
        if wk_list[i - 1] == 0:
            change_rate = 0
        else:
            change_rate = round((wk_list[i] - wk_list[i - 1]) * 100 / wk_list[i - 1], 2)
        wk_change_rate_list.append(str(change_rate))

    wk_str = ";".join(wk_change_rate_list)
    print(share_code, value_type + "_rate", len(wk_change_rate_list))

    # 把计算值写入DB
    cl.sql = "DELETE FROM `Cacl_Values_TBL` WHERE ( share_code = '{}' and data_type = '{}_rate')". \
        format(share_code, value_type)
    cl.exec_update_sql()

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('{}', '{}_rate', '{}')".format(share_code, value_type, wk_str)
    cl.exec_update_sql()


def cacl_high_low_gap(share_code, from_date, standard_count_of_days=0):
    cl = a0_functions.RunSQL()

    # 查询当日高价
    cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
             " share_code = '{}' ORDER by trade_date ".format('high_price', from_date, share_code)
    cl.exec_select_sql()
    wk_high_price_list = [i[0] for i in cl.out_list]
    while len(wk_high_price_list) < standard_count_of_days:
        wk_high_price_list.insert(0, 0.00)

    # 查询当日低价
    cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
             " share_code = '{}' ORDER by trade_date ".format('low_price', from_date, share_code)
    cl.exec_select_sql()
    wk_low_price_list = [i[0] for i in cl.out_list]
    while len(wk_low_price_list) < standard_count_of_days:
        wk_low_price_list.insert(0, 0.00)

    # 查询收盘价
    cl.sql = "SELECT {} FROM `DailyShareInfo` where trade_date >= '{}' and" \
             " share_code = '{}' ORDER by trade_date ".format('finishi_price', from_date, share_code)
    cl.exec_select_sql()
    wk_finishi_price_ist = [i[0] for i in cl.out_list]
    while len(wk_finishi_price_ist) < standard_count_of_days:
        wk_finishi_price_ist.insert(0, 0.00)

    # 1日之内的涨跌幅
    wk_oneday_change_rate_list = []
    for i in range(1, standard_count_of_days):
        if wk_finishi_price_ist[i - 1] == 0:
            wk_oneday_change_rate = 0
        else:
            wk_oneday_change_rate = round(
                100 * (wk_high_price_list[i] - wk_low_price_list[i]) / wk_finishi_price_ist[i - 1], 2)
        wk_oneday_change_rate_list.append(str(wk_oneday_change_rate))

    wk_str = ";".join(wk_oneday_change_rate_list)
    print(share_code, 'oneday_change_rate', len(wk_oneday_change_rate_list))

    # 把值写入DB
    cl.sql = "DELETE FROM `Cacl_Values_TBL` WHERE ( share_code = '{}' and data_type = '{}')". \
        format(share_code, 'oneday_change_rate')
    cl.exec_update_sql()

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('{}', 'oneday_change_rate', '{}')".format(share_code, wk_str)
    cl.exec_update_sql()


def calc_all_values(share_code, from_date, standard_count_of_days=0):
    cl = a0_functions.RunSQL()

    cl.sql = "SELECT  `start_price`, `high_price`, `low_price`, `finishi_price`, `trade_total` FROM " \
             "`DailyShareInfo` WHERE `trade_date` > '{}' and `share_code`= '{}'".format(from_date, share_code)
    cl.exec_select_sql()

    wk_start_price_list = [i[0] for i in cl.out_list]
    wk_high_price_list = [i[1] for i in cl.out_list]
    wk_low_price_list = [i[2] for i in cl.out_list]
    wk_finishi_price_list = [i[3] for i in cl.out_list]
    wk_trade_total_list = [i[4] for i in cl.out_list]

    while len(wk_start_price_list) < standard_count_of_days:
        wk_start_price_list.insert(0, '0.00')
    while len(wk_high_price_list) < standard_count_of_days:
        wk_high_price_list.insert(0, '0.00')
    while len(wk_low_price_list) < standard_count_of_days:
        wk_low_price_list.insert(0, '0.00')
    while len(wk_finishi_price_list) < standard_count_of_days:
        wk_finishi_price_list.insert(0, '0.00')
    while len(wk_trade_total_list) < standard_count_of_days:
        wk_trade_total_list.insert(0, '0.00')

    # 收盘价
    wk_list = [str(i) for i in wk_finishi_price_list]
    del (wk_list[0])
    str_finishi_price = ";".join(wk_list)

    # 成长幅度
    wk_list = []
    for i in range(1, standard_count_of_days):
        if decimal.Decimal(wk_finishi_price_list[-1]) == 0:
            wk_rate = 0
        else:
            wk_rate = round(100 * decimal.Decimal(wk_finishi_price_list[i]) /
                            decimal.Decimal(wk_finishi_price_list[-1]), 2)
        wk_list.append(str(wk_rate))
    str_growth_rete = ";".join(wk_list)

    # 涨跌幅
    wk_list = []
    for i in range(1, standard_count_of_days):
        if decimal.Decimal(wk_finishi_price_list[i - 1]) == 0:
            wk_rate = 0
        else:
            wk_rate = round((decimal.Decimal(wk_finishi_price_list[i]) - decimal.Decimal(wk_finishi_price_list[i - 1]))
                            * 100 / decimal.Decimal(wk_finishi_price_list[i - 1]), 2)
        wk_list.append(str(wk_rate))
    str_finishi_price_change_rate = ";".join(wk_list)

    # 涨跌额
    wk_list = []
    for i in range(1, standard_count_of_days):
        wk_price_change = decimal.Decimal(wk_finishi_price_list[i]) - decimal.Decimal(wk_finishi_price_list[i - 1])
        wk_list.append(str(wk_price_change))
    str_price_change = ";".join(wk_list)

    # 高低幅
    wk_list = []
    for i in range(1, standard_count_of_days):
        if decimal.Decimal(wk_finishi_price_list[i - 1]) == 0:
            wk_rate = 0
        else:
            wk_rate = round((decimal.Decimal(wk_high_price_list[i]) - decimal.Decimal(wk_low_price_list[i])) * 100 /
                            wk_finishi_price_list[i - 1], 2)
        wk_list.append(str(wk_rate))
    str_inday_price_change_rate = ";".join(wk_list)

    # 成交金额
    wk_list = []
    for i in range(1, standard_count_of_days):
        wk_trade_money = decimal.Decimal(wk_finishi_price_list[i]) * decimal.Decimal(wk_trade_total_list[i])
        wk_list.append(str(wk_trade_money))
    str_total_trade_money = ";".join(wk_list)

    json_list = [{"close_price": str_finishi_price,
                  "finishi_price_change_rate": str_finishi_price_change_rate,
                  "price_change": str_price_change,
                  "inday_price_change_rate": str_inday_price_change_rate,
                  "total_trade_money": str_total_trade_money,
                  "str_growth_rete": str_growth_rete
                  }]

    json_array = json.dumps(json_list, ensure_ascii=False)
    # 把值写入DB
    cl.sql = "delete from Cacl_Values_TBL where  ( share_code = '{}' and data_type = '{}')".format(share_code,
                                                                                                   "json")
    cl  .exec_update_sql()

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) " \
             "VALUES ('{}', '{}', '{}')".format(share_code, 'json', json_array)
    cl.exec_update_sql()


def set_all_values():
    get_all_date_and_share()
    print("Start ....")
    cl = a0_functions.RunSQL()
    cl.sql = "select data_json from Cacl_Values_TBL where data_type = 'date_ref' "
    cl.exec_select_sql()
    date_ref = str(cl.out_list[0][0].split(";")[0])
    standard_count_of_days = int(cl.out_list[0][0].split(";")[3])

    cl.sql = "select data_json from Cacl_Values_TBL where data_type = 'all_share_code' "
    cl.exec_select_sql()
    share_code_list = cl.out_list[0][0].split(";")

    for i in share_code_list:
        # calc_values(i, 'finishi_price', date_ref, standard_count_of_days)
        # cacl_change_rates(i, 'finishi_price', date_ref, standard_count_of_days)
        # cacl_high_low_gap(i, date_ref, standard_count_of_days)
        calc_all_values(i, date_ref, standard_count_of_days)
        print("done! ", i)
    print("Finished ....")


# get_all_date_and_share()
# # calc_values('4055', 'finishi_price', '2019-09-17')
# cacl_change_rates('4055', 'finishi_price', '2019-09-17', 240)
# cacl_high_low_gap('4055', '2019-09-17', 240)
set_all_values()

calc_all_values('4055', '2019-09-17', 240)
