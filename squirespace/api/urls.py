from django.conf.urls import url
from api import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^author/(?P<pk>[\w-]+)/posts', views.UserPosts.as_view()),
    url('^author/$', views.UserList.as_view()),
    url('^author/(?P<pk>[\w-]+)', views.UserDetail.as_view()),
    url('^posts/(?P<pk>[\w-]+)/comments', views.PostDetailComments.as_view()),
    url('^posts/(?P<pk>[\w-]+)', views.PostDetail.as_view()),
    url('^posts/$', views.PostList.as_view()),
    url('^author/posts', views.UserViewablePosts.as_view()),
    url('^friends/(?P<pk>[\w-]+)/$', views.UsersFriends.as_view()),
    url('^friends/(?P<pk1>[0-9A-Fa-f-]+)/(?P<pk2>[0-9A-Fa-f-]+)/$', views.AreTheseTwoUsersFriends.as_view()),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

