"""定义myapp1的URL模式"""
from django.conf.urls import url, include
from . import views

urlpatterns = [

    # 显示所有的主题
    url(r'^$', views.share, name='share'),

]

