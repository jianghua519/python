from django.shortcuts import render

from .models import Basiccompanyinfo, CacheTable


# Create your views here.

def share(request):
    # """显示股票列表"""
    # json1 = CaclValuesTbl.objects.get(share_code='1001')
    #
    # # 查询结果要用字段名来表示
    # # 用json解析之后,是list
    # text = json.loads(json1.data_json)
    #
    # # 传给网页的只能是字典
    # return render(request, 'myapp2/share_detail.html', text[0])

    # allcompany = Basiccompanyinfo.objects.order_by('company_marketname', 'industry')
    allcompany = Basiccompanyinfo.objects.raw(
        'select share_code, share_name ,industry, company_marketname from BasicCompanyInfo')

    CacheTable.objects.filter(cache_lable='sharecodelist').delete()
    wk_list = [i.share_code for i in allcompany]
    sharecodelist = CacheTable(cache_lable='sharecodelist', cache_content=";".join(wk_list))
    sharecodelist.save()

    context = {'allcompany': allcompany}
    return render(request, 'myapp2/companylist.html', context)


def share_detail(request, share_code):
    """显示某只股票信息"""
    context = {}
    s1 = Basiccompanyinfo.objects.get(share_code=share_code)
    context['share'] = s1

    cache = CacheTable.objects.get(cache_lable='sharecodelist')

    sharecodelist = cache.cache_content.split(';')
    i = sharecodelist.index(share_code)

    if i == 0:
        context["prev"] = {'share_code': 'None'}
    else:
        context["prev"] = {'share_code': sharecodelist[i - 1]}

    if i == len(sharecodelist) - 1:
        context["next"] = {'share_code': 'None'}
    else:
        context["next"] = {'share_code': sharecodelist[i + 1]}

    # json1 = CaclValuesTbl.objects.get(share_code=share_code)

    # 查询结果要用字段名来表示ss
    # 用json解析之后,是list
    # text = json.loads(json1.data_json)

    # 传给网页的只能是字典
    # return render(request, 'myapp2/share_detail.html', text[0])
    return render(request, 'myapp2/share_detail.html', context)
