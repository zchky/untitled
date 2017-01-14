from django.conf.urls import url

from .import views
import wechat_sdk

app_name='weixin'
urlpatterns = [
    # ex: /polls/
    url(r'^test',views.wechat,name='weixin'),
]
