import a0_functions as a0
from bs4 import BeautifulSoup
import time


class Selectors:
    selectlist1 = {
        "share_code": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > dl > dt",
        "share_name": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > table > tbody > tr > th > h1",
        "industry": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > dl > dd.category.yjSb > a",
        "current_price": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > table > tbody > tr >  td:nth-child(3)",
        "current_price_time": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > dl > dd.yjSb.real > span",
        "changed": "#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > table > tbody > tr > td.change ",
        "yestoday_price": "#detail > div.innerDate > div:nth-child(1) > dl > dd > strong",
        "start_price": "#detail > div.innerDate > div:nth-child(2) > dl > dd > strong",
        "high_price": "#detail > div.innerDate > div:nth-child(3) > dl > dd > strong",
        "low_price": "#detail > div.innerDate > div:nth-child(4) > dl > dd > strong",
        "total_trade_share": "#detail > div.innerDate > div:nth-child(5) > dl > dd > strong",
        "total_trade_money": "#detail > div.innerDate > div:nth-child(6) > dl > dd > strong",
        "limit_price": "#detail > div.innerDate > div:nth-child(7) > dl > dd > strong",
        "company_total_market_price": "#rfindex > div.chartFinance > div:nth-child(1) > dl > dd > strong",
        "company_total_share": "#rfindex > div.chartFinance > div:nth-child(2) > dl > dd > strong",
        "return_rate": "#rfindex > div.chartFinance > div:nth-child(3) > dl > dd > strong",
        "return_per_share": "#rfindex > div.chartFinance > div:nth-child(4) > dl > dd > strong > a",
        "return_yymm": "#rfindex > div.chartFinance > div:nth-child(4) > dl > dd > span",
        "per": "#rfindex> div.chartFinance > div:nth-child(5) > dl > dd > strong",
        "pbr": "#rfindex> div.chartFinance > div:nth-child(6) > dl > dd > strong",
        "eps1": "#rfindex> div.chartFinance > div:nth-child(7) > dl > dd > strong > a",
        "eps2": "#rfindex> div.chartFinance > div:nth-child(8) > dl > dd > strong > a",
        "eps_wk": "#rfindex> div.chartFinance > div:nth-child(8) > dl > dd > span",
        "high_price_thisyear": "#rfindex > div.chartFinance > div:nth-child(11) > dl > dd",
        "high_price_thisyear_date": "#rfindex > div.chartFinance > div:nth-child(11) > dl > dd > span",
        "low_price_thisyear": "#rfindex > div.chartFinance > div:nth-child(12) > dl > dd",
        "low_price_thisyear_date": "#rfindex > div.chartFinance > div:nth-child(11) > dl > dd > span",
        "credit_buy": "#margin > div > div.main2colL.clearFix > div:nth-child(1) > dl > dd",
        "credit_sale": "#margin > div > div.main2colR.clearFix > div:nth-child(1) > dl > dd",
    }
    selectlist2 = {
        "company_summary1": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td:nth-child(2)",
        "company_summary2": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(14) > td:nth-child(4)",
        "company_summary3": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(15)",
        "english_name": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(7) > td:nth-child(2)",
        "company_create_date": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(9) > td:nth-child(2)",
        "Company_MarketName": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(10) > td:nth-child(2)",
        "company_share_open_date ": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(11) > td:nth-child(2)",
        "kesan": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(12) > td:nth-child(2)",
        "company_address": "#pro_body > center > div.profile > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)",
    }


def soup_select(soup, in_dict, out_dict):
    for i in in_dict.keys():
        a = soup.select(in_dict[i])
        if len(a) > 0:
            if a[0].string is None:
                out_string = a[0].text.replace("\n", " ")
            else:
                out_string = a[0].string
        else:
            out_string = ""
        if i == "company_address":
            out_string = out_string.replace("[周辺地図]", "")
        out_dict[i] = out_string


def accecc_yahoo(str_share_code):
    s = Selectors()
    wk_dict = {}

    yahoo_url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=" + str_share_code + ".T"
    yahoo_html = a0.download_html(yahoo_url)
    soup = BeautifulSoup(yahoo_html, "html5lib")

    soup_select(soup, s.selectlist1, wk_dict)

    if wk_dict["share_name"] == "" or wk_dict["current_price"] == "---":
        print(str_share_code, "not found,または　株価は取得エラー")
        return

    yahoo_url = "https://profile.yahoo.co.jp/fundamental/" + str_share_code
    yahoo_html = a0.download_html(yahoo_url)
    soup = BeautifulSoup(yahoo_html, "html5lib")

    soup_select(soup, s.selectlist2, wk_dict)

    if not wk_dict["company_summary1"] == "":
        wk_dict["company_summary"] = wk_dict["company_summary1"] + ". 従業員数 " + \
                                     wk_dict["company_summary2"] + "," + wk_dict["company_summary3"]
    else:
        wk_dict["company_summary"]= ""

    del (wk_dict["company_summary1"])
    del (wk_dict["company_summary2"])
    del (wk_dict["company_summary3"])

    wk_dict["eps2"] = wk_dict["eps2"] + wk_dict["eps_wk"]
    del (wk_dict["eps_wk"])

    keys = []
    values = []
    for i in wk_dict.keys():
        keys.append(i)
        values.append("'" + wk_dict[i] + "'")

    rs = a0.RunSQL()
    rs.sql = "DELETE FROM `BasicCompanyInfo2` WHERE share_code  = '{}'".format(wk_dict["share_code"])
    rs.exec_update_sql()
    rs.sql = "insert into BasicCompanyInfo2 ( {} ) VALUES ({})".format(", ".join(keys), ", ".join(values))
    # print(rs.sql)
    rs.exec_update_sql()


company_list = a0.get_share_code_list_from_daily_price_db()
# company_list = [["1406"]]
print("所有公司数:", len(company_list))
j = 0
for i in company_list:
    j = j + 1
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "No.=", j, ",Share code=", i[0])
    accecc_yahoo(i[0])
