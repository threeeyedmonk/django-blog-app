from django.urls import path
from blog import views
from django.conf.urls import url

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('createpost/', views.createpost, name='createpost'),
    url(r'^(?P<pk>[-\w]+)/$', views.PostDetailView.as_view(), name='postdetail')
]
