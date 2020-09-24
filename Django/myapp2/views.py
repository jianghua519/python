import logging

from django.shortcuts import render
from .models import CaclValuesTbl


# Create your views here.

def share(request):
    """显示所有的主题"""
    json = CaclValuesTbl.objects.get(share_code='2501')
    # print(json)
    logging.info(json)
    context = {'json': json}
    return render(request, 'myapp2/json.html', context)
