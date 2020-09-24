import json
import logging

from django.shortcuts import render
from .models import CaclValuesTbl


# Create your views here.

def share(request):
    """显示所有的主题"""
    json1 = CaclValuesTbl.objects.get(share_code='1001')

    # 查询结果要用字段名来表示
    # 用json解析之后,是list
    text = json.loads(json1.data_json)

    # 传给网页的只能是字典
    return render(request, 'myapp2/json.html', text[0])
