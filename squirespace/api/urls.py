from django.conf.urls import url
from api import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^api/author/$', views.UserList.as_view()),
    url(r'^api/author/(?P<pk>\d+)', views.UserDetail.as_view()),
    url(r'^api/posts/(?P<pk>\d+)/comments', views.Comments.as_view()),
    url(r'^api/posts/(?P<pk>\d+)', views.PostDetail.as_view()),
    url(r'^api/posts/$', views.PostList.as_view()),

    

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

