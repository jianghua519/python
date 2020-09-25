import json
import logging

from django.shortcuts import render
from .models import CaclValuesTbl, Basiccompanyinfo


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

    allcompany = Basiccompanyinfo.objects.order_by('company_marketname', 'industry')

    context = {'allcompany': allcompany}
    return render(request, 'myapp2/companylist.html', context)


def share_detail(request, share_code):
    """显示某只股票信息"""
    json1 = CaclValuesTbl.objects.get(share_code=share_code)

    # 查询结果要用字段名来表示
    # 用json解析之后,是list
    text = json.loads(json1.data_json)

    # 传给网页的只能是字典
    return render(request, 'myapp2/share_detail.html', text[0])
