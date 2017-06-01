from django.conf.urls import include,url
from .import views

urlpatterns=[
    url(r'^zc/$',views.post_list ,name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^upload/',views.upload_file,name='upload_file'),
    url(r'^lab/',views.lab,name='lab'),
    url(r'^aboutme/$',views.about_me,name='about_me'),
    url(r'^zc/archive/(?P<archive_name>.*)/$',views.post_list_archive,name='post_list_archive'),
    url(r'^search/$', views.post_search, name='post_search'),
    url(r'^test/$',views.test,name='test'),
    url(r'^scene_update_url/$',views.scene_update_view , name='scene_update_url'),

]