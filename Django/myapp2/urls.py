"""定义myapp1的URL模式"""
from django.conf.urls import url, include
from . import views

urlpatterns = [

    # 显示股票列表
    url(r'^$', views.share, name='share'),

    # 显示股票详细信息
    url(r'^(?P<share_code>\d+)/$', views.share_detail, name='share_detail'),

    # 添加关注
    url(r'^add_follow/(?P<share_code>\d+)/$', views.add_follow, name='add_follow'),

    # 删除关注
    url(r'^delete_follow/(?P<share_code>\d+)/$', views.delete_follow, name='delete_follow'),

    # 显示测试网页
    url(r'^test$', views.test, name='test'),

]

