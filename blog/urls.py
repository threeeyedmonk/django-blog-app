from django.urls import path
from blog import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('createpost/', views.createpost, name='createpost'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='postdetail'),
    url(r'^profile/post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name = 'profile_postdetail'),
    url(r'^profile/$', views.UserProfileView.as_view(), name = 'userprofile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
