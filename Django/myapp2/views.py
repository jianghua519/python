import datetime

from django.shortcuts import render, redirect

from .models import Basiccompanyinfo, CacheTable, FollowTable


# Create your views here.

def share(request):
    print(request.GET.get("from"))
    # 取得预先定义的list的list
    list_by_code = CacheTable.objects.filter(cache_lable__contains='～')
    wk_list = [i.cache_lable for i in list_by_code]
    context = {"lists": wk_list}

    # 取得预先定义的industry的list
    list_by_industry = CacheTable.objects.filter(cache_lable__contains=')')
    wk_list = [i.cache_lable for i in list_by_industry]
    context["lists_industry"] = wk_list

    # 取得关注的list
    context["follows"] = "关注的股票({})".format(FollowTable.objects.count())

    # 如果需要, 更新 CacheTable的follow record
    if request.GET.get("from") == "follow":
        follows = FollowTable.objects.all()
        wk_follow_list = []
        for i in follows:
            bc = Basiccompanyinfo.objects.get(share_code=i.share_code)
            one = ",".join([bc.share_code, bc.share_name, bc.industry, bc.company_marketname])
            wk_follow_list.append(one)
        CacheTable.objects.filter(cache_lable="follow").delete()
        CacheTable(cache_lable="follow", cache_content=";".join(wk_follow_list)).save()

    # 取得要表示的list
    allcompany = []

    if "from" in request.GET:
        context['from'] = request.GET.get("from")
        list_by_code = CacheTable.objects.get(cache_lable=request.GET.get("from"))
        wk_list = list_by_code.cache_content.split(';')
    else:
        context['from'] = list_by_code[0].cache_lable
        wk_list = list_by_code[0].cache_content.split(';')

    for i in wk_list:
        j = i.split(',')
        wk_dict = {'share_code': j[0],
                   'share_name': j[1],
                   'industry': j[2],
                   'company_marketname': j[3]
                   }
        allcompany.append(wk_dict)
    context['allcompany'] = allcompany

    # print(context.keys())
    return render(request, 'myapp2/companylist.html', context)


def share_detail(request, share_code):
    """显示某只股票信息"""
    context = {}
    s1 = Basiccompanyinfo.objects.get(share_code=share_code)

    # 修改会社概要　
    s1.company_summary = s1.company_summary.split("の会社概要。")[1]
    context['share'] = s1

    # 查询归属列表里的前后股票
    cache = CacheTable.objects.get(cache_lable=request.GET.get("from"))
    wk_list = cache.cache_content.split(';')
    sharecodelist = [i.split(',')[0] for i in wk_list]

    i = sharecodelist.index(share_code)
    if i == 0:
        context["prev"] = {'share_code': 'None'}
    else:
        context["prev"] = {'share_code': sharecodelist[i - 1]}

    if i == len(sharecodelist) - 1:
        context["next"] = {'share_code': 'None'}
    else:
        context["next"] = {'share_code': sharecodelist[i + 1]}

    # 查询归属列表里的前后股票
    context["from"] = request.GET.get("from")

    follow = FollowTable.objects.filter(share_code=share_code)
    print(follow)
    context["follow"] = follow

    # 传给网页的只能是字典
    return render(request, 'myapp2/share_detail.html', context)


def add_follow(request, share_code):
    bc = Basiccompanyinfo.objects.get(share_code=share_code)

    new_follow = FollowTable(share_code=share_code)
    new_follow.follow_date = datetime.datetime.now()
    new_follow.price_at_follow_time = float(bc.current_price.replace(',', ''))
    new_follow.follow_comment = "通过网页关注"
    new_follow.save()

    url = "/share/" + share_code + "?from=" + request.GET.get("from")
    return redirect(url)


def delete_follow(request, share_code):
    FollowTable.objects.filter(share_code=share_code).delete()

    url = "/share/" + share_code + "?from=" + request.GET.get("from")
    return redirect(url)


def test(request):
    context = {"test": "test"}
    return render(request, 'myapp2/test.html', context)
