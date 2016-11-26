from django.conf.urls import url
from . import views
# from views import UserRegPage
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>[0-9A-Fa-f-]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>[0-9A-Fa-f-]+)/delete/$', views.post_delete, name='post_delete'),
	url(r'^reg/$',views.register,name='register'),
	url(r'^reg/confirm/$', views.registration_complete, name = 'registration_complete'),
	url(r'^git/$',views.gitregister,name='gitregister'),
	url(r'^git/confirm/$', views.git_registration_complete, name = 'git_registration_complete'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/$', views.profile, name='profile'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/friend_request_sent/$', views.send_friend_request, name='send_friend_request'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/friend_request_cancelled/$', views.cancel_friend_request, name='cancel_friend_request'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/friend_request_accepted/$', views.accept_friend_request, name='accept_friend_request'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/friend_request_rejected/$', views.reject_friend_request, name='remove_friend'),
	url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/friend_removed/$', views.remove_friend, name='remove_friend'),
	url(r'^post/(?P<pk>[0-9A-Fa-f-]+)/$', views.post_detail, name='post_detail'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [url(r'^.*$', views.page_not_found, name='404')]


