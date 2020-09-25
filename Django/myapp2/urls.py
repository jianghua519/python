"""定义myapp1的URL模式"""
from django.conf.urls import url, include
from . import views

urlpatterns = [

    # 显示股票列表
    url(r'^$', views.share, name='share'),

    # 显示股票详细信息
    url(r'^(?P<share_code>\d+)/$', views.share_detail, name='share_detail'),

]

