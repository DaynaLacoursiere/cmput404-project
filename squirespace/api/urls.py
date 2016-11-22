from django.conf.urls import url
from api import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^author/(?P<pk>\d+)/posts', views.UserPosts.as_view()),
    url('^author/$', views.UserList.as_view()),
    url('^author/(?P<pk>\d+)', views.UserDetail.as_view()),
    url('^posts/(?P<pk>\d+)/comments', views.PostDetailComments.as_view()),
    url('^posts/(?P<pk>\d+)', views.PostDetail.as_view()),
    url('^posts/$', views.PostList.as_view()),
    url('^author/posts', views.UserViewablePosts.as_view()),

    

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

