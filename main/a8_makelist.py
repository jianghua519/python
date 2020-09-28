import a0_functions

rs = a0_functions.RunSQL()

# 取得股票列表
rs.sql = "select share_code, share_name ,industry, company_marketname from BasicCompanyInfo where industry != ' '"
rs.exec_select_sql()

wk_dict = {}
k = " "
for i in range(1, len(rs.out_list)+1):
    if i in (1, 501, 1001, 1501, 2001, 2501, 3001, 3501, 4001, 4501, 5001, 5501):
        k = str(rs.out_list[i - 1][0]) + "～"
        wk_dict[k] = ",".join(rs.out_list[i - 1])
    else:
        wk_dict[k] = wk_dict[k] + ";" + ",".join(rs.out_list[i - 1])

rs.sql = "delete from Cache_Table where cache_lable like '%～'"
rs.exec_update_sql()

for i in wk_dict.keys():
    rs.sql = "INSERT INTO `Cache_Table` (`id`, `cache_lable`, `cache_content`) " \
             "VALUES (NULL, '{}', '{}')".format(i, wk_dict[i])
    rs.exec_update_sql()


# 取得股票列表(按业种)
rs.sql = "select industry , count(*) " \
         "from BasicCompanyInfo where industry != ' ' group  by industry"
rs.exec_select_sql()

#业种list
wk_list = rs.out_list


wk_dict = {}
k = " "

for i in wk_list:
    rs.sql = "select share_code, share_name ,industry, company_marketname from BasicCompanyInfo where industry ='{}'".format(i[0])
    rs.exec_select_sql()

    lable = str(i[0] + '('+str(i[1])+')')
    content = []
    for j in range(0, len(rs.out_list)):
        content.append(",".join(rs.out_list[j]))
    print(i[0], i[1], str(len(content)))
    rs.sql = "delete from Cache_Table where cache_lable like '{}'".format(lable)
    rs.exec_update_sql()
    rs.sql = "INSERT INTO `Cache_Table` (`id`, `cache_lable`, `cache_content`) " \
             "VALUES (NULL, '{}', '{}')".format(lable, ';'.join(content))
    rs.exec_update_sql()

