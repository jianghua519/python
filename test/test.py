# from main import CommonTools
import json
import matplotlib.pyplot as plt
import a0_functions
import a0_functions as ct


def test1():
    out_list = []
    out_csv_path = '//jianghuanas/Downloads/ShareAnalyze/Data/test/test.csv'
    ct.db_to_list_and_csv("select share_code, share_name,industry,current_price,yestoday_price,total_trade_money,"
                          "company_total_market_price,Company_Share_Open_Date,company_summary from BasicCompanyInfo;",
                          out_list=out_list, out_csv_path=out_csv_path)
    print(len(out_list))


def test2():
    # sql = "SELECT `trade_date`, `share_code`,  `start_price`, `high_price`, `low_price`, " \
    #       "`finishi_price`, `trade_total` FROM `DailyShareInfo` WHERE trade_date > '2019/1/1' " \
    #       "order BY share_code , trade_date; "
    # 检索前300天的日期
    sql = "SELECT DISTINCT trade_date FROM `DailyShareInfo` ORDER by trade_date DESC LIMIT 0, 300"
    out_list = []
    ct.db_to_list_and_csv(sql, out_list)

    # 把日期转换为json格式
    out_list2 = []
    for i in out_list:
        out_list2.append(i[0].strftime("%Y-%m-%d"))
    print(out_list2)
    out_list2.reverse()
    min_date = out_list2[0]
    current_date = out_list2[299]

    jsonArr = json.dumps(out_list2, ensure_ascii=False)
    # print(out_list[0])
    print(jsonArr)

    # 把日期存储到DB
    tsql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) VALUES ('0000', 'date', '{json}')"
    sql = tsql.format(json=jsonArr)
    ct.db_to_list_and_csv(sql)

    # 得到股票列表
    sql = "SELECT  share_code FROM `DailyShareInfo` where trade_date = '" + current_date + "'"
    print(sql)
    out_list = []
    ct.db_to_list_and_csv(sql, out_list)
    print(out_list)
    for i in out_list:
        sql = "SELECT  finishi_price FROM `DailyShareInfo` where trade_date >= '" + min_date + \
              "' and share_code = '" + str(i[0]) + "' ORDER by trade_date DESC"
        print(sql)
        out_list2 = []
        ct.db_to_list_and_csv(sql, out_list2)
        print(out_list2[0][0], ",", len(out_list2))


def test3():
    cl = a0_functions.RunSQL()

    # 分析的天数
    count_of_days = 100

    # 检索前300天的日期
    cl.sql = "SELECT DISTINCT trade_date FROM `DailyShareInfo` ORDER by trade_date DESC LIMIT 0, " + str(count_of_days)
    cl.exec_select_sql()

    # 把日期转换为json格式
    wk_list = [i[0].strftime("%Y-%m-%d") for i in cl.out_list]
    wk_list.reverse()
    ref_date = wk_list[0]
    first_date = wk_list[1]
    current_date = wk_list[-1]
    del (wk_list[0])
    # print(wk_list)
    # strValues = json.dumps(wk_list, ensure_ascii=False)

    # 把Json写到DB
    cl.sql = "DELETE FROM `Cacl_Values_TBL`"
    cl.exec_update_sql()

    strValues = ";".join(wk_list)

    cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) VALUES ('0000', 'date', '{json}')"
    cl.sql = cl.sql.format(json=strValues)
    cl.exec_update_sql()

    # 得到股票列表
    cl.sql = "SELECT  share_code FROM `DailyShareInfo` where trade_date = '" + current_date + "'"
    cl.exec_select_sql()
    share_list = [str(i[0]) for i in cl.out_list]

    # 循环处理每一支股票
    for share_code in share_list:
        # 得到收盘价
        cl.sql = "SELECT  finishi_price FROM `DailyShareInfo` where trade_date >= '" + ref_date + \
                 "' and share_code = '" + share_code + "' ORDER by trade_date "
        cl.exec_select_sql()

        # 把收盘价转换为json格式
        wk_list = [str(i[0]) for i in cl.out_list]

        del (wk_list[0])
        # strValues = json.dumps(wk_list, ensure_ascii=False)
        strValues = ";".join(wk_list)
        cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) VALUES ('" + \
                 share_code + "', 'finish_price', '{json}') "
        cl.sql = cl.sql.format(json=strValues)
        cl.exec_update_sql()

        # 计算涨跌幅
        wk_list = [i[0] for i in cl.out_list]
        wk_change_rate_list = []
        for i in range(1, len(wk_list)):
            if wk_list[i - 1] == 0:
                change_rate = 0
            else:
                change_rate = round((wk_list[i] - wk_list[i - 1]) / wk_list[i - 1], 4)
            wk_change_rate_list.append(change_rate)
        # strValues = json.dumps([str(i) for i in wk_change_rate_list], ensure_ascii=False)
        strValues = ";".join([str(i) for i in wk_change_rate_list])
        cl.sql = "INSERT INTO `Cacl_Values_TBL`(`share_code`, `data_type`, `data_json`) VALUES ('" + \
                 share_code + "', 'change_rate', '{json}') "
        cl.sql = cl.sql.format(json=strValues)
        cl.exec_update_sql()
        # return


def test4():
    cl = a0_functions.RunSQL()

    cl.sql = "select data_json  from Cacl_Values_TBL  where data_type = 'date'"
    cl.exec_select_sql()
    list1 = str(cl.out_list[0][0]).split(";")

    # cl.sql = "select data_json  from Cacl_Values_TBL  where share_code = '1001' and data_type = 'finishi_price_rate'"
    # cl.exec_select_sql()
    # list2 = [float(x) for x in (str(cl.out_list[0][0])).split(";")]
    #
    # cl.sql = "select data_json  from Cacl_Values_TBL  where share_code = '9603' and data_type = 'finishi_price_rate'"
    # cl.exec_select_sql()
    # list3 = [float(x) for x in (str(cl.out_list[0][0])).split(";")]
    # list3 = [float(x) for x in (str(cl.out_list[0][0])).split(";")]

    cl.sql = "select data_json  from Cacl_Values_TBL  where share_code = '8256' " \
             "and data_type = 'oneday_change_rate'"
    cl.exec_select_sql()
    list3 = [float(x) for x in (str(cl.out_list[0][0])).split(";")]

    cl.sql = "select data_json  from Cacl_Values_TBL  where share_code = '9603' " \
             "and data_type = 'oneday_change_rate'"
    cl.exec_select_sql()
    list4 = [float(x) for x in (str(cl.out_list[0][0])).split(";")]

    plt.title("Change rate from " + list1[0] + " - " + list1[-1])
    plt.xlabel("Date")
    plt.ylabel("Change rate")

    # plt.plot(list1, list2, label='nikei rate')
    plt.plot(list1, list3, label='9414 rate in a day')
    plt.plot(list1, list4, label='9603 rate in a day')
    plt.legend()  # 显示图例, 图例中内容由 label 定义
    # plt.grid()  # 显示网格

    plt.gcf().autofmt_xdate()

    plt.show()


# test4()
sql = "select * from Cacl_Values_TBL where share_code = '9603'"
out_csv_path = "test.txt"


a0_functions.db_to_list_and_csv(sql, out_csv_path=out_csv_path)
