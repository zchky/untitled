from django.conf.urls import url

from . import views

app_name='pydrone'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^push/',views.push,name='push'),
    url(r'^base/', views.base, name='base'),
    url(r'^online_plot/',views.online_plot,name='online_plot'),
    url(r'^main/', views.main, name='main'),
    url(r'^online_map/',views.online_map,name='online_map'),
    url(r'^offline_plot/',views.offline_plot,name='offline_plot'),
    url(r'^offline_map/',views.offline_map,name='offline_map'),
    # url(r'^add/',views.add,name='add'),
    # ex: /polls/5/
]
