from lxml import etree
import platform, os

import a0_functions


def get_research_com_info():
    if str(platform.platform())[0:3] == "Win":
        str_pathprifix = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/CompanyInfoFiles/C"
    else:
        str_pathprifix = "/volume1/Downloads/ShareAnalyze/Data/CompanyInfoFiles/C"

    i = 1001
    while i < 10000:
        out_file_name = str_pathprifix + str(i) + ".html"
        url1 = "https://xn--vckya7nx51ik9ay55a3l3a.com/companies/" + str(i)
        # url1 = "https://上場企業サーチ.com/companies/" + str(i)
        a0_functions.func_download_data(url1, out_file_name)
        i = i + 1


def analyze_html(strHTMLFileName):
    dom = etree.HTML(open(strHTMLFileName).read())
    work_list = []

    a_text = dom.xpath('//div[@class="company-name"]/h2/text()[1]')
    work_list = work_list + a_text
    # print("社名,"+str(a_text).replace("\\n\\t\\t\\t", ""))

    a_text = dom.xpath('//*[contains(text(), "上場市場")]/../../tr[2]/td[1]/a/text()')
    work_list = work_list + a_text
    # print("上場市場,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "上場日")]/../../tr[2]/td[2]/text()')
    work_list = work_list + a_text
    # print("上場日,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "業種")]/following-sibling::dd[1]/a/text()')
    work_list = work_list + a_text
    # print("業種,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "本店所在地")]/following-sibling::dd[1]/div/a/text()')
    work_list = work_list + a_text
    # print("本店所在地,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "決算日")]/following-sibling::dd[1]/text()')
    work_list = work_list + a_text
    # print("決算日,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "時価総額")]/following-sibling::dd[1]/text()')
    work_list = work_list + a_text
    # print("時価総額,"+str(a_text))

    a_text = dom.xpath('//*[contains(text(), "コーポレートサイトURL")]/following-sibling::dd[1]/a/text()')
    work_list = work_list + a_text
    # print("コーポレートサイトURL,"+str(a_text))
    # print("")
    print(",".join(work_list).replace("\\n\\t\\t\\t", "").replace("	", ""))


def get_info_from_html():
    if str(platform.platform())[0:3] == "Win":
        strPathprifix = "//JIANGHUANAS/Downloads/ShareAnalyze/Data/CompanyInfoFiles/C"
    else:
        strPathprifix = "/volume1/Downloads/ShareAnalyze/Data/CompanyInfoFiles/C"

    i = 1000
    j = 1
    while i < 10000:
        outfilename = strPathprifix + str(i) + ".html"
        if os.path.isfile(outfilename):
            analyze_html(outfilename)
            # print(str(j)+",Start to Process file ",outfilename)
            j = j + 1
        i = i + 1


# 下载所有网页
get_research_com_info()
# 分析所有网页
get_info_from_html()
