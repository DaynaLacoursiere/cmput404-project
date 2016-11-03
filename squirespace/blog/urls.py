from django.conf.urls import url
from . import views
from views import UserRegPage
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
	url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
	url(r'^reg/$', UserRegPage.as_view()),
	url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout')
]

