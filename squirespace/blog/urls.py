from django.conf.urls import url
from . import views
# from views import UserRegPage
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
	url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
	url(r'^reg/$',views.register,name='register'),
	url(r'^reg/confirm/$', views.registration_complete, name = 'registration_complete'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^profile/(?P<pk>\d+)/$', views.profile, name='profile'),
	url(r'^friends/$', views.show_friends, name='friends'),
	url(r'^send_friend_request/(?P<pk>\d+)/$', views.send_friend_request, name="send_friend_request")

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




